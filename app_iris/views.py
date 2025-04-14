from django.views import View
from django.shortcuts import render
from app_iris.models import IrisModel
from app_iris.validations import IrisValidations
from django.contrib import messages
import traceback

class IrisListView(View):
    def get(self, request):
        context = {
            'data_set': IrisModel.objects.all()
        }
        return render(request, 'app_iris/list.html', context=context)

class IrisCreateView(View):
    def get(self, request):
        return render(request, 'app_iris/create.html')
    
    def post(self, request):
        try:
            iris = IrisValidations()
            iris.set_sepal_length(float(request.POST.get('sepal_length')[0]))
            iris.set_sepal_width(float(request.POST.get('sepal_width')[0]))
            iris.set_petal_length(float(request.POST.get('petal_length')[0]))
            iris.set_petal_width(float(request.POST.get('petal_width')[0]))
            iris.set_specie(request.POST.get('specie'))

            model = iris.to_model()
            model.save()
        except:
            # tratativa de erro
            traceback.print_exc()
        
        return render(request, 'app_iris/create.html')

class IrisUpdateView(View):
    def get(self, request, id):
        try:
            iris_instance = IrisModel.objects.get(id=int(id))
            context = {
                'data': iris_instance,  
                'species': ['setosa', 'versicolor', 'virginica']
            }
            return render(request, 'app_iris/update.html', context)
        except IrisModel.DoesNotExist:
            messages.error(request, 'Íris não encontrada.')
            return redirect('iris_list')  

    def post(self, request, id):
        try:
            iris_instance = IrisModel.objects.get(id=int(id))

            iris = IrisValidations()
            iris.set_sepal_length(float(request.POST.get('sepal_length')))
            iris.set_sepal_width(float(request.POST.get('sepal_width')))
            iris.set_petal_length(float(request.POST.get('petal_length')))
            iris.set_petal_width(float(request.POST.get('petal_width')))
            iris.set_specie(request.POST.get('specie'))

            iris_instance.sepal_length = iris.get_sepal_length()
            iris_instance.sepal_width = iris.get_sepal_width()
            iris_instance.petal_length = iris.get_petal_length()
            iris_instance.petal_width = iris.get_petal_width()
            iris_instance.specie = iris.get_specie()
            iris_instance.save()

            messages.success(request, 'Dados atualizados com sucesso!')
            return redirect('iris_list')
        except Exception as e:
            traceback.print_exc()
            messages.error(request, f'Ocorreu um erro: {str(e)}')
            return render(request, 'app_iris/update.html', {'data': IrisModel.objects.get(id=id), 'species': ['setosa', 'versicolor', 'virginica']})



class IrisDashboardView(View):
    def get(self, request):
        context = {
            'setosa': 5, 
            'versicolor': 6, 
            'virginica': 4
        }
        return render(request, 'app_iris/dashboard.html', context)