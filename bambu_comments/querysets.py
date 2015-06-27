from django.db import models

class CommentQuerySet(models.query.QuerySet):
    """A custom queryset adding an extra bit of functinoality to the default"""

    def live(self):
        """Returns only approved comments not marked as spam"""

        return self.filter(
            approved = True,
            spam = False
        )
