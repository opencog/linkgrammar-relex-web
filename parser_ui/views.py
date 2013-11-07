# Create your views here.
from _socket import inet_aton
from telnetlib import Telnet
import json
import socket
import sys

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages

from parser_ui.forms import SubmitSentenceForm
from parser_ui.models import Server


LANGUAGES = {
    'en': 'English',
    'ru': 'Russian',
    'de': 'German',
    'rx': 'RelEx'
}

VERSIONS = {
    'dev': 'Development',
    'rel': 'Release',
    'smp': 'Simple',
    'ocg': 'OpenCog',
    'sfd': 'Stanford-Compatibility-Mode'
}

SERVERS = [
    ('en', 'rel'),
    ('en', 'dev'),
    ('ru', 'rel'),
    ('rx', 'smp'),
    ('rx', 'ocg'),
    ('rx', 'sfd')
]


def _telnet(ip, port, input):
    tn = Telnet(ip, port)
    tn.write(input + '\n')
    output = ''
    try:
        output = tn.read_all()
    except:
        print 'error in reading telnet response...'
        tn.close()
        raise
    tn.close()
    return output

def xnetcat(hostname, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.sendall(content + '\n')
    # s.shutdown(socket.SHUT_WR)
    output = 'ola'
    while True:
        output += 'enter read loop'
        data = s.recv(1024)
        if data == "":
            output += 'got EOF'
            break
        output += 'got this buf' + data
        # print "Received:", repr(data)
        print "duude Received:", data
    s.close()
    print "Connection closed. full return was:", output
    sys.stdout.flush()
    return output


def index(request):
    if request.method == 'POST':

        form = SubmitSentenceForm(request.POST)
        if not form.is_valid():
            return render_to_response('index.html', RequestContext(request, {'form': form, 'layout': 'vertical'}))

        # sentence = str(form.cleaned_data['type_in_a_sentence'])
        sentence = unicode(form.cleaned_data['type_in_a_sentence'])
        language = form.cleaned_data['language']
        version = form.cleaned_data['choose_version']
        number_of_linkages_to_show = int(request.POST.get('number_of_linkages_to_show', 5))
        options = request.POST.getlist('options')
        relex = {'smp': None, 'ocg': None, 'sfd': None}

        if language == 'en':
            for relex_version in request.POST.getlist('relex'):
                server_object = Server.objects.get(language='rx', version=relex_version)
                # relex[relex_version] = _telnet(server_object.ip, server_object.port, sentence)
                relex[relex_version] = xnetcat(server_object.ip, server_object.port, sentence)
            request.session['relex'] = relex

        server_object = Server.objects.get(language=language, version=version)
        # parsed_value = _telnet(server_object.ip, server_object.port,
        #                       'storeDiagramString:true,text:' + sentence)
        parsed_value = xnetcat(server_object.ip, server_object.port,
                               'storeDiagramString:true,text:' + sentence)
        lines = parsed_value.split("\n", 1)
        request.session['parse_response'] = "duuude xnetcat split said>>", lines, "<<wtf"

        return redirect('/parse_result')
# xxxxxxxxxxxxxx
        parsed_value = lines[1]
        try:
            parsed_value = json.loads(parsed_value)
        except:
            print 'error in parsing JSON response...'
            parse_response = ['An error occurred while trying to parse the sentence...']
            raise
        parse_response = []
        for iteration, linkage in enumerate(parsed_value['linkages']):
            if not 'al' in options and iteration == number_of_linkages_to_show:
                break
            result = linkage['diagramString']
            if 'ct' in options:
                result += linkage['constituentString']
            parse_response.append(result)
        request.session['parse_response'] = parse_response

        return redirect('/parse_result')
    if 'settings_saved' in request.session and request.session['settings_saved']:
        messages.success(request, 'Server settings saved successfully')
        request.session['settings_saved'] = False
    form = SubmitSentenceForm(initial={'language': 'en', 'choose_version': 'rel'})
    return render_to_response('index.html', RequestContext(request, {'form': form, 'layout': 'vertical'}))


def parse_result(request, page):
    lines = request.session['parse_response']
    paginator = Paginator(lines, 1)
    page = request.GET.get('page')
    try:
        show_lines = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        show_lines = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        show_lines = paginator.page(paginator.num_pages)
    return render_to_response(
        'parse_result.html',
        RequestContext(
            request,
            {
                'result': show_lines,
                'relex_simple': request.session['relex']['smp'],
                'relex_opencog': request.session['relex']['ocg'],
                'relex_stanford': request.session['relex']['sfd']
            }
        )
    )


def settings(request):
    servers = {}
    for language, version in SERVERS:
            servers[LANGUAGES[language] + '-' + VERSIONS[version]] =\
                Server.objects.get(language=language, version=version)

    if request.method == 'POST':
        error = False
        for name in servers:
            server = servers[name]
            ip = request.POST.get(name + '-ip')
            port = request.POST.get(name + '-port')
            try:
                inet_aton(ip)
            except:
                messages.error(request, 'Invalid IP address for ' + name + ', changes discarded')
                error = True
                break
            try:
                port = int(port)
            except:
                messages.error(request, 'Invalid Port number for ' + name + ', changes discarded')
                error = True
                break
            if len(str(port)) not in [4, 5]:
                messages.error(request, 'Invalid Port number for ' + name + ', changes discarded')
                error = True
                break
            server.ip, server.port = ip, port
            server.save()
        if not error:
            request.session['settings_saved'] = True
            return redirect('index')

    server_names = sorted(servers.keys())
    result = []
    for name in server_names:
        result.append((name, servers[name].ip, servers[name].port))
    return render_to_response('settings.html', RequestContext( request,{'result': result}))
