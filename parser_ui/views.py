# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from telnetlib import Telnet
import json
from django.template.context import RenderContext
from parser_ui.forms import SubmitSentenceForm


EN_SERVER = 'localhost', 1234


def index(request):
    if request.method == 'POST':

        form = SubmitSentenceForm(request.POST)
        if not form.is_valid():
            return render_to_response('index.html', RequestContext(request, {'form': form, 'layout': 'vertical'}))

        sentence = str(form.cleaned_data['type_in_a_sentence'])
        tn = Telnet(*EN_SERVER)
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