from django.shortcuts import render
from instagram.utils import login_decorator


class FeedView(View):  # returns all instagram feeds on main page
    @login_decorator
    def get(self, request):
        user = request.user
        feeds = user.feed_set.values()
        return JsonResponse(feeds, status=200)


class PostView(View):
    # get method: returns a single instagram post
    def get(self, request):
        # post method: writes and uploads a single post

    def post(self, request):


class CommentView(View):
    # get method: PERHAPS return all abbreviated comments for a post?
    def get(self, request):
        # post method: leaves a single comment on a post

    def post(self, request):
