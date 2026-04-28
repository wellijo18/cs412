# rate_the_plate/views.py
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Car, Review, ReviewReaction, Comment
from django.urls import reverse
from .forms import CreateReviewForm, CreateCommentForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class AuthForMixin(LoginRequiredMixin):
    def get_login_url(self):
        return reverse('login')


class CarListView(ListView):
    model = Car
    template_name = 'rate_the_plate/show_all_cars.html'
    context_object_name = 'cars'

    def get_queryset(self):
        queryset = Car.objects.all()

        self.state = self.request.GET.get('state', '')
        self.license_plate = self.request.GET.get('license_plate', '')

        if not self.state and not self.license_plate:
            return Car.objects.none()

        if self.state:
            queryset = queryset.filter(state__iexact=self.state.strip())

        if self.license_plate:
            queryset = queryset.filter(license_plate__icontains=self.license_plate.strip())

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['state'] = self.request.GET.get('state', '')
        context['license_plate'] = self.request.GET.get('license_plate', '')
        return context


class CarDetailView(DetailView):
    model = Car
    template_name = 'rate_the_plate/show_car.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(car=self.object)

        for review in reviews:
            review.like_count = ReviewReaction.objects.filter(review=review, reaction='like').count()
            review.dislike_count = ReviewReaction.objects.filter(review=review, reaction='dislike').count()

        context['reviews'] = reviews
        return context


class ReviewDetailView(DetailView):
    model = Review
    template_name = 'rate_the_plate/show_review.html'
    context_object_name = 'review'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = self.object

        context['comments'] = Comment.objects.filter(review=review)
        context['like_count'] = ReviewReaction.objects.filter(review=review, reaction='like').count()
        context['dislike_count'] = ReviewReaction.objects.filter(review=review, reaction='dislike').count()

        if self.request.user.is_authenticated:
            context['user_reaction'] = ReviewReaction.objects.filter(
                user=self.request.user,
                review=review
            ).first()

        return context


class MyAccountView(AuthForMixin, ListView):
    model = Review
    template_name = 'rate_the_plate/my_account.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        reviews = Review.objects.filter(user=self.request.user)

        for review in reviews:
            review.like_count = ReviewReaction.objects.filter(review=review, reaction='like').count()
            review.dislike_count = ReviewReaction.objects.filter(review=review, reaction='dislike').count()
            review.comments = Comment.objects.filter(review=review)

        return reviews


class CreateReviewView(AuthForMixin, CreateView):
    form_class = CreateReviewForm
    template_name = 'rate_the_plate/create_review_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car'] = Car.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        car = Car.objects.get(pk=self.kwargs['pk'])
        form.instance.car = car
        form.instance.user = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('review', kwargs={'pk': self.object.pk})


class UpdateReviewView(AuthForMixin, UpdateView):
    '''view to update a review'''
    model = Review
    form_class = CreateReviewForm
    template_name = 'rate_the_plate/update_review_form.html'
    context_object_name = 'review'

    def get_success_url(self):
        return reverse('review', kwargs={'pk': self.object.pk})


class DeleteReviewView(AuthForMixin, DeleteView):
    '''view to delete a review'''
    model = Review
    template_name = 'rate_the_plate/delete_review_form.html'
    context_object_name = 'review'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = self.object
        context['review'] = review
        context['car'] = review.car
        return context

    def get_success_url(self):
        return reverse('car', kwargs={'pk': self.object.car.pk})


class CreateCommentView(AuthForMixin, CreateView):
    form_class = CreateCommentForm
    template_name = 'rate_the_plate/create_comment_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review'] = Review.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        review = Review.objects.get(pk=self.kwargs['pk'])
        form.instance.review = review
        form.instance.user = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('review', kwargs={'pk': self.object.review.pk})


class AddReactionView(AuthForMixin, TemplateView):
    template_name = None

    def dispatch(self, request, *args, **kwargs):
        review = Review.objects.get(pk=self.kwargs['pk'])

        if 'dislike' in request.path:
            reaction_type = 'dislike'
        else:
            reaction_type = 'like'

        ReviewReaction.objects.update_or_create(
            user=request.user,
            review=review,
            defaults={'reaction': reaction_type}
        )

        return redirect('review', pk=review.pk)


class RemoveReactionView(AuthForMixin, TemplateView):
    template_name = None

    def dispatch(self, request, *args, **kwargs):
        review = Review.objects.get(pk=self.kwargs['pk'])
        ReviewReaction.objects.filter(user=request.user, review=review).delete()
        return redirect('review', pk=review.pk)