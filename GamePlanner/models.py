from django.db import models
from django.contrib.auth.models import AbstractUser
from .slugify import unique_slugify
import math
import datetime
class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)


class Project(models.Model):
    HOURS = "HOURS"
    DAYS = "DAYS"
    POINTS = "POINTS"
    COST_METRIC_CHOICES = (
        (HOURS, 'Hours'),
        (DAYS, 'Days'),
        (POINTS, 'Points'),
    )
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_projects", null=True, blank=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    creation_date = models.DateTimeField('Creation Time', auto_now_add=True)
    description = models.TextField('Project Description')
    project_info = models.TextField('General Project Information')
    cost_metric = models.CharField(max_length=2, choices=COST_METRIC_CHOICES, default=HOURS)
    def save(self, *args, **kwargs):
        # Only save slugs on first save
        if not self.id:
            print(self.name)
            unique_slugify(self, self.name)
        super(Project, self).save(*args,**kwargs)

    def get_pending_tasks(self):
        return self.tasks.all().exclude(completion_date__isnull=False)

    def get_closed_tasks(self):
        return self.tasks.all().exclude(completion_date__isnull=True)
    def get_estimated_cost(self):
        cost = 0
        for task in self.tasks.all():
            cost += task.estimated_cost
        return cost

    def get_final_cost(self):
        cost = 0
        for task in self.tasks.all():
            cost += task.final_cost
        return cost

    def get_remaining_cost(self):
        remaining_cost =  self.get_estimated_cost() - self.get_final_cost()
        if remaining_cost < 0:
            remaining_cost = 0
        return remaining_cost

    def format_cost(self, cost):
        if self.cost_metric == self.HOURS:
            final_string = "{} {}"
            minutes, hours = math.modf(cost)

            hours_string = ""
            minutes_string = ""

            if hours > 0:
                hours_string = "{}h".format(int(hours))
            if minutes > 0:
                minutes_string = "{}m".format(int(minutes*60))

            if minutes <= 0 and hours <= 0:
                final_string = "0h"

            return final_string.format(hours_string, minutes_string).strip()
    def __str__(self):
        return self.name
class Platform(models.Model):
    name = models.CharField(max_length=200)
    platform = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="platforms", null=True, blank=True)
    def __str__(self):
        return self.name

class Milestone(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField('Project Description')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="milestones", null=True, blank=True)
    creation_date = models.DateTimeField('Creation Time', auto_now_add=True)
    starting_date = models.DateTimeField('Starting Date')
    due_date = models.DateTimeField('Due Date')
    closing_date = models.DateTimeField('Closing Date')

class ProjectUserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_users_data")
    is_admin = models.BooleanField("Is an administrator", default=False)
    is_active = models.BooleanField("Is the user active", default=False)
    join_date = models.DateTimeField('Joining date', auto_now_add=True)
    def __str__(self):
        return self.user.username
class Category(models.Model):
    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="categories")
    creation_date = models.DateTimeField('Creation Time', auto_now_add=True)

class SubCategory(models.Model):
    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    creation_date = models.DateTimeField('Creation Time', auto_now_add=True)

class Stage(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="stages")
    is_unblocker = models.BooleanField()
    creation_date = models.DateTimeField('Creation date', auto_now_add=True)

class DesignElement(models.Model):
    name = models.CharField(max_length=300)


class Task(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField('Task Description')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks", blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    design_element = models.ForeignKey(DesignElement, on_delete=models.CASCADE, related_name="design_elements")
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    estimated_cost = models.FloatField("Estimated time cost")
    final_cost = models.FloatField("Final cost")
    due_date = models.DateTimeField('Due Date')
    creation_date = models.DateTimeField('Creation date', auto_now_add=True)
    completion_date = models.DateTimeField('Completion date', null=True, blank=True)
    update_date = models.DateTimeField('Last update date')
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_tasks")
    def save():
        super(models.Model,self).save()
