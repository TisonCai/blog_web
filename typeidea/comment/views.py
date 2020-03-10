from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from comment.forms import CommentForm
# Create your views here.

class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')
        print('tagget:{}'.format(target))
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.save()
            succeed = True
            return redirect(target)
        else:
            succeed = False

        context = {
            'form': comment_form,
            'target': target,
            'succeed': succeed,
        }
        return self.render_to_response(context)

