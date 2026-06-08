from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin


class AuthorRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        book = self.get_object()
        user = self.request.user

        if user.is_superuser:
            return True

        if user.groups.filter(name='Модераторы').exists():
            return True

        return book.author_user == user

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для редактирования этой книги.')
        return redirect('home')