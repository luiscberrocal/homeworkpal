__author__ = 'lberrocal'

class AbstractProjectCreateUpdateMixin(object):
    formset_class = None

    def get_context_data(self, **kwargs):
        assert self.formset_class is not None, "No formset class specified"
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['line_formset'] = self.formset_class(
                self.request.POST,
                instance=self.object)
        else:
            context['line_formset'] = self.formset_class(
                instance=self.object)
        return context

    # def get_form(self, form_class=None):
    #     """Restrict the form relations to the current organization"""
    #     form = super().get_form(form_class)
    #     orga = organization_manager.get_selected_organization(self.request)
    #     self.restrict_fields_choices_to_organization(form, orga)
    #     return form

    def form_valid(self, form):
        context = self.get_context_data()
        line_formset = context['line_formset']
        if not line_formset.is_valid():
            return super().form_invalid(form)

        self.object = form.save()
        line_formset.instance = self.object
        line_formset.save()

        return super().form_valid(form)
