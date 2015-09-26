from bambu_comments.querysets import *
from bambu_mail.shortcuts import render_to_mail
from django.conf import settings
from django.contrib.contenttypes import fields as generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
import requests, logging

AKISMET_URL = 'http://%s.rest.akismet.com/1.1/comment-check'
LOGGER = logging.getLogger('bambu_comments')

class CommentQuerySet(models.QuerySet):
    """A custom queryset adding an extra bit of functinoality to the default"""

    def live(self):
        """Returns only approved comments not marked as spam"""

        return self.filter(
            approved = True,
            spam = False
        )

class Comment(models.Model):
    """A comment posted on an object"""

    name = models.CharField(max_length = 50)
    """The commenter's name"""

    website = models.URLField(max_length = 255, null = True, blank = True)
    """The commenter's website URL"""

    email = models.EmailField(max_length = 255, db_index = True)
    """The commenter's email address"""

    sent = models.DateTimeField(auto_now_add = True, db_index = True)
    """The date the comment was sent"""

    approved = models.BooleanField(default = False, db_index = True)
    """Set to ``True`` when the comment is approved"""

    spam = models.BooleanField(default = False, db_index = True)
    """Set to ``True`` when the comment has been marked as spam"""

    body = models.TextField()
    """The sanitised body of the comment"""

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index = True)
    content_object = generic.GenericForeignKey()
    objects = CommentQuerySet.as_manager()

    def __unicode__(self):
        return u'Re: %s' % unicode(self.content_object)

    def get_absolute_url(self):
        """
        The URL is taken by calling ``get_absolute_url()`` on the parent object, and adding a
        '#comment-x' suffix, where 'x' is the comment ID
        """

        return self.content_object.get_absolute_url() + '#comment-%d' % self.pk

    def check_for_spam(self, request):
        """Checks for spam via Akismet (requires the ``AKISMET_KEY`` setting to be a non-empty string)"""

        akismet = getattr(settings, 'AKISMET_KEY', '')
        if not akismet:
            return False

        LOGGER.debug('Checking comment for spam')
        ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('USER_AGENT')
        referrer = request.META.get('HTTP_REFERER')

        site = Site.objects.get_current()
        response = requests.post(AKISMET_URL % akismet,
            data = {
                'blog': 'http://%s/' % (site.domain),
                'user_ip': ip,
                'user_agent': user_agent,
                'referrer': referrer,
                'permalink': 'http://%s%s' % (site.domain, self.content_object.get_absolute_url()),
                'comment_type': 'comment',
                'comment_author': self.name,
                'comment_author_email': self.email,
                'comment_author_url': self.website,
                'comment_content': self.body
            }
        )

        if response.content == 'true':
            return True

        if response.content == 'false':
            return False

        LOGGER.warn('Unexpected response from Akismet: %s' % response.content)

    def save(self, *args, **kwargs):
        notify = kwargs.pop('notify', True)

        if self.spam:
            self.approved = False

        new = not self.pk and not self.spam
        if new and not self.approved and not self.spam:
            self.approved = Comment.objects.filter(
                email__iexact = self.email,
                approved = True,
                spam = False
            ).exists()

        super(Comment, self).save(*args, **kwargs)

        if new and notify:
            render_to_mail(
                u'New comment submitted',
                'comments/mail.txt',
                {
                    'comment': self,
                    'author': self.content_object.author
                },
                self.content_object.author
            )

    class Meta:
        ordering = ('-sent',)
        get_latest_by = 'sent'
        db_table = 'comments_comment'
        app_label = 'bambu_comments'
