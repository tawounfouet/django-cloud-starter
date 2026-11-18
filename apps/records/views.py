from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import RecordForm
from .models import Record


class OwnedRecordsMixin:
    model = Record

    def get_queryset(self):
        return Record.objects.filter(created_by=self.request.user)


class RecordListView(LoginRequiredMixin, OwnedRecordsMixin, ListView):
    template_name = "records/record_list.html"
    context_object_name = "records"


class RecordDetailView(LoginRequiredMixin, OwnedRecordsMixin, DetailView):
    template_name = "records/record_detail.html"
    context_object_name = "record"


class RecordCreateView(LoginRequiredMixin, CreateView):
    model = Record
    form_class = RecordForm
    template_name = "records/record_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("record_detail", kwargs={"pk": self.object.pk})


class RecordUpdateView(LoginRequiredMixin, OwnedRecordsMixin, UpdateView):
    form_class = RecordForm
    template_name = "records/record_form.html"

    def get_success_url(self):
        return reverse("record_detail", kwargs={"pk": self.object.pk})


class RecordDeleteView(LoginRequiredMixin, OwnedRecordsMixin, DeleteView):
    template_name = "records/record_confirm_delete.html"
    success_url = reverse_lazy("record_list")
