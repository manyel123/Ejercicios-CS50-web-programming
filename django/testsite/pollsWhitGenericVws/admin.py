from django.contrib import admin

from .models import Question, Choice

# StackedInline for displaying separated choices(uses more space)
# TabularInline for displaying choices in a tabular space(uses less space, similar to a table format)
# This class will displays choices to add them into a question
class ChoiceInline(admin.TabularInline):
    # Choice model is related with question model by a foreignkey
    model = Choice

    # Number of fields for choices that are meant to display
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    # fieldsets group the model information for a better looking
    fieldsets = [
        # field for question title(question_text)
        (None,                  {'fields': ['question_text']}),
        # field for date information which group and collapse all date information
        ('Date information',    {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]

    # display ChoiceInline bellow date information with 3 fields for adding different choices
    inlines = [ChoiceInline]

    # displays all 3 options in the question header also allows to order the first 2 options
    # for the boolean option, an aditional decorator in Question model is required
    list_display = ('question_text', 'pub_date', 'was_published_recently')

    # displays a filter list based on dates
    list_filter = ['pub_date']

    # displays a search bar for searching at questions
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)

