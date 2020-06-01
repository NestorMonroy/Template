from django.utils.http import is_safe_url
from django.http import Http404, HttpResponse, HttpResponseRedirect


class NextUrlMixin(object):
    default_next = "/"

    def get_next_url(self):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        # print(redirect_path)
        if is_safe_url(redirect_path, request.get_host()):
            return redirect_path
        return self.default_next


class RequestFormAttachMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestFormAttachMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return super(LoginRequiredMixin, self)\
                .dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')


# class ProjectPermRequired(LoginRequiredMixin):
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.has_perm('timesheets.approve_timesheet'):
#             return super(ProjectPermRequired, self).dispatch(request, *args, **kwargs)
#         else:
#             return HttpResponseRedirect('/')


# class AmbassadorPermRequired(LoginRequiredMixin):
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.has_perm('timesheets.add_timesheet'):
#             return super(AmbassadorPermRequired, self).dispatch(request, *args, **kwargs)
#         else:
#             return HttpResponseRedirect('/')
