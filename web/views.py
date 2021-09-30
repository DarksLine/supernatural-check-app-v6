from django.http.response import HttpResponseRedirect
from django.urls import reverse

from django.shortcuts import render, redirect
from .engine_module import *
from .storage_module import storage
from django.views.generic import View


class InitialView(View):
    def get(self, request):

        request.session.save()
        request.session.modified = True

        return render(request, 'initial.html')

    def post(self, request):
        count_psychics = int(request.POST['count'])

        the_list_psychics = PsychicList()
        the_list_psychics.create_list_psychics(count_psychics)

        storage.save(session_key=request.session.session_key, obj=the_list_psychics)

        return HttpResponseRedirect(reverse('testing_url'))


class TestingView(View):
    def get(self, request):
        the_list_psychics = storage.load(session_key=request.session.session_key)

        view_list = []
        for psy in the_list_psychics.list_psychics:
            psy.try_predict_number()
            view_list.append({
                'name': psy.name,
                'guess': psy.predict_number[-1]
            })

        storage.save(session_key=request.session.session_key, obj=the_list_psychics)

        return render(request, 'testing.html', {'list_res': view_list})

    def post(self, request):
        number = int(request.POST['answer'])
        the_list_psychics = storage.load(session_key=request.session.session_key)

        for psy in the_list_psychics.list_psychics:
            psy.result_predict(number)

        gamer = User()
        gamer.get_user_number(number)

        storage.save(session_key=request.session.session_key, obj=the_list_psychics)
        storage.save_user(session_key=request.session.session_key, user=gamer)
        return redirect('/result')


class ResultView(View):
    def get(self, request):
        the_list_psychics = storage.load(session_key=request.session.session_key)
        gamer = storage.load_user(session_key=request.session.session_key)

        user_numbers = gamer.user_number
        view_list = the_list_psychics.get_complete_dict()

        # вызвать функцию, которая построит таблицу ответов экстрасенсов
        # вызвать функцию, которая построит список ответов пользователя

        # for psy in the_list_psychics.list_psychics:
        #     view_list.append({
        #         'name': psy,
        #         'guess': psy.predict_number,
        #         'success': psy.success / len(psy.predict_number) * 100
        #     })

        return render(request, 'result.html', {
            'dict_psy': view_list,
            'user_list': user_numbers
        })
