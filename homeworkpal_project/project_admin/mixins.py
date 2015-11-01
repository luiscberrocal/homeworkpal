__author__ = 'lberrocal'

class AbstractProjectCreateUpdateMixin(object):
    formset_classes = None

    def get_context_data(self, **kwargs):
        assert self.formset_classes is not None, "No formset class specified"
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            for formset_class in self.formset_classes:
                context[formset_class[0]] = formset_class[1](
                    self.request.POST,
                    instance=self.object)
        else:
            for formset_class in self.formset_classes:
                context[formset_class[0]] = formset_class[1](
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
        for formset_class in self.formset_classes:
            line_formset = context[formset_class[0]]
            if not line_formset.is_valid():
                return super().form_invalid(form)
        i = 1
        for formset_class in self.formset_classes:
            line_formset = context[formset_class[0]]
            if i == 1:
                self.object = form.save()
            line_formset.instance = self.object
            line_formset.save()
            i += 1

        return super().form_valid(form)
