from django.shortcuts import render

from django.views.generic import (
    ListView,
    DetailView,
)


class MerchandiseListView(ListView):
    template_name = 'blog/article_list.html'
    queryset = Article.objects.all()  # blog/<modelname>_list.html


class MerchandiseDetailView(DetailView):
    template_name = 'blog/article_detail.html'
    # queryset = Article.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Article, id=id_)
