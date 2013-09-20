# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from telnetlib import Telnet
import json
from parser_ui.forms import SubmitSentenceForm
from parser_ui.models import Server


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
        except:
            print 'error in parsing JSON response...'
            parse_response = ['An error occurred while trying to parse the sentence...']
            raise
        return parse_result(request, parse_response)
    form = SubmitSentenceForm()
    return render_to_response('index.html', RequestContext(request, {'form': form, 'layout': 'vertical'}))


def parse_result(request, result):
    return render_to_response('parse_result.html', RequestContext(request, {'result': result}))


def settings(request):
    servers = {}
    for language in LANGUAGES:
        for version in VERSIONS:
            servers[language + '-' + version] = Server.objects.get(language=language, version=version)

    if request.method == 'POST':
        return 
