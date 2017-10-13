from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
import json
from glob import glob
import time
import os
import base64


def index(request):
    listProcess = []

    p = os.popen('df -h | grep data')
    result = list(map(
        lambda x: list(filter(lambda xx: xx, x.split(' '))),
        p.read().split("\n")
    ))
    p.close()
    tempRow = []
    for item in result:
        if not item:
            continue

        tempRow.append({
            "name": item[0].split('/')[-1].replace('1', ''),
            "rate": item[4]
        })
        if len(tempRow) == 3:
            listProcess.append(tempRow)
            tempRow = []
    if tempRow:
        listProcess.append(tempRow)
    return render(request, 'Downloads/index.html', {"listProcess": listProcess})


def table(request):
    datas = list()
    topic, date = request.GET.get('topic'), request.GET.get('date')
    if topic and date:
        for i in glob(r'/data/*/*/%s/*%s*.tgz' % (topic.strip(), date)):
            datas.append({
                'name': i.split('/')[-1],
                'date': FmtDatetime("%Y-%m-%d %H:%M:%S", int(os.stat(i).st_atime)),
                'size': NumberFmt(os.stat(i).st_size),
                'path': base64.encodestring(i)
            })

    return HttpResponse(json.dumps({'data': datas}), content_type="application/json")


def downFile(request):
    if request.GET.get('path') and request.GET.get('name'):
        def file_iterator(file_name, chunk_size=512):
            with open(file_name) as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        response = StreamingHttpResponse(file_iterator(base64.decodestring(request.GET.get('path'))))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(request.GET.get('name'))

        return response
    else:
        return HttpResponse(json.dumps(''), content_type="application/json")


def FmtDatetime(fmt, timescamp):
    time_local = time.localtime(timescamp)
    return time.strftime(fmt, time_local)


def NumberFmt(number):
    if number >= 912680550:
        return str(round(number / 1073741824, 2)) + " GB"
    elif number >= 891289:
        return str(round(number / 1048576, 2)) + " MB"
    elif number >= 870:
        return str(round(number / 1024, 2)) + " KB"
    else:
        return str(round(number, 2)) + " B"
