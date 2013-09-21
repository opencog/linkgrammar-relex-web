# Create your views here.
from _socket import inet_aton
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from telnetlib import Telnet
import json
from parser_ui.forms import SubmitSentenceForm
from parser_ui.models import Server
from django.contrib import messages


LANGUAGES = {
    'en': 'English',
    'ru': 'Russian',
    'de': 'German'
}

VERSIONS = {
    'dev': 'Development',
    'rel': 'Release'
}

def index(request):
    if request.method == 'POST':

        form = SubmitSentenceForm(request.POST)
        if not form.is_valid():
            return render_to_response('index.html', RequestContext(request, {'form': form, 'layout': 'vertical'}))

        sentence = str(form.cleaned_data['type_in_a_sentence'])
        language = form.cleaned_data['language']
        version = form.cleaned_data['choose_version']
        server_object = Server.objects.get(language=language, version=version)
        tn = Telnet(server_object.ip, server_object.port)
        tn.write('storeDiagramString:true,text:' + sentence + '\n')
        parsed_value = ''
        try:
            parsed_value = tn.read_all()
        except:
            print 'error in reading telnet response...'
            raise
        tn.close()
        lines = parsed_value.split("\n", 1)
        parsed_value = lines[1]
        parsed_value = json.loads(parsed_value)
        parse_response = []
        try:
            for linkage in parsed_value['linkages']:
                parse_response.append(linkage['diagramString'] + linkage['constituentString'])
            request.session['parse_response'] = parse_response
        except:
            print 'error in parsing JSON response...'
            parse_response = ['An error occurred while trying to parse the sentence...']
            raise
        return redirect('/parse_result')
    form = SubmitSentenceForm()
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
    return render_to_response('parse_result.html', RequestContext(request, {
        'result': show_lines,
    }))


def settings(request):
    servers = {}
    for language in LANGUAGES:
        for version in VERSIONS:
            servers[LANGUAGES[language] + '-' + VERSIONS[version]] =\
                Server.objects.get(language=language, version=version)

    if request.method == 'POST':
        error = False
        for name in servers:
            server = Server()
            ip = request.POST.get(name + '-ip')
            port = request.POST.get(name + '-port')
            try:
                inet_aton(ip)
            except:
                messages.error(request, 'Invalid IP address for ' + name)
                error = True
                break
            try:
                port = int(port)
            except:
                messages.error(request, 'Port left empty in ' + name)
                error = True
                break
            if len(port) not in [4, 5]:
                messages.error(request, 'Invalid Port number for ' + name)
                error = True
                break
            server.ip, server.port = ip, port
            server.save()
        if not error:
            request.session['settings_saved'] = True

    server_names = servers.keys().sort()
    result = []
    for name in server_names:
        result.append((name, servers[name].ip, servers[name].port))
    return render_to_response('settings.html', RequestContext(request, {'result': result}))