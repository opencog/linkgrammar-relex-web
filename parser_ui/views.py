# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from telnetlib import Telnet
import json



def index(request):
    if request.method == 'POST':
        sentence = str(request.POST.get('txt_sentence'))
        ip = str(request.POST.get('server_ip'))
        port = int(request.POST.get('server_port'))
        tn = Telnet(ip, port)
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
        parse_response = 'An error occurred while trying to parse the sentence...'
        try:
            parse_response = parsed_value['linkages'][0]['diagramString'] +\
                             parsed_value['linkages'][0]['constituentString']
        except:
            print 'error in parsing JSON response...'
            raise
        return render_to_response('index.html',
                                  {'show_result': True, 'sentence': sentence,
                                   'parse_response': parse_response})
    return render_to_response('index.html', context_instance=RequestContext(request))