from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import slugify


# Create your models here.
class Tournament(models.Model):
    year = models.CharField(max_length=99)
    title = models.CharField(max_length=99, blank=True)
    slug = models.SlugField(blank=True)
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.year + ' ' + self.title)
        super(Tournament, self).save(*args, **kwargs)

    def __str__(self):
        return self.year


class Team(models.Model):
    COLORS = (
        ('Black', 'Nero'),
        ('Silver', 'Argento'),
        ('Gray', 'Grigio'),
        ('White', 'Bianco'),
        ('Maroon', 'Amaranto'),
        ('Red', 'Rosso'),
        ('Orange', 'Arancione'),
        ('Purple', 'Viola'),
        ('Fuchsia', 'Fucsia'),
        ('Green', 'Verde Scuro'),
        ('Lime', ' Verde Lime'),
        ('Yellow', 'Giallo'),
        ('Navy', 'Blue Navy'),
        ('Blue', 'Blu'),
        ('Teal', 'Verde Acqua'),
        ('Azure', 'Azzurro'),
        ('Pink', 'Rosa'))
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True, related_name='teams')
    name = models.CharField(max_length=999)
    short_name = models.CharField(max_length=12, blank=True)
    city = models.CharField(max_length=36, blank=True)
    slug = models.SlugField(blank=True)
    color = models.CharField(max_length=16, choices=COLORS, default='White', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.name = self.name.title()
        self.short_name = self.short_name.title()
        self.city = self.city.title()
        super(Team, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class AllStarGame(models.Model):
    name = models.CharField(max_length=16)
    rules = models.CharField(max_length=999, blank=True)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(AllStarGame, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Human(models.Model):
    SHIRT_SIZES = (('XXS', 'XXS'), ('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'))
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    jersey_size = models.CharField(max_length=4, choices=SHIRT_SIZES, blank=True)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.first_name + ' ' + self.last_name)
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()
        super(Human, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Player(Human):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    year_of_birth = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)], blank=True, null=True)
    jersey_number = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)], blank=True, null=True)
    all_star_game = models.ForeignKey(AllStarGame, on_delete=models.SET_NULL, blank=True, null=True, related_name='players')


class Coach(Human):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='coaches')
    cell_number = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    email = models.EmailField(max_length=64, blank=True, null=True)


class Stage(models.Model):  # Fase
    name = models.CharField(max_length=16, blank=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='stages')
    precedent_stage = models.OneToOneField('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='next_stage')
    protected = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Group(models.Model):  # Girone
    name = models.CharField(max_length=16, blank=True)
    FORMAT_TYPES = (('Round-Robin', "All'italiana"), ('Elimination', 'Ad eliminazione'))
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='groups')
    format = models.CharField(max_length=32, choices=FORMAT_TYPES, default='Round-Robin')
    number_of_teams = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    importance = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return self.name + ' - ' + self.stage.name


class Round(models.Model):  # Giornata
    round = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='rounds')

    def __str__(self):
        return str(self.round)


class Match(models.Model):  # Partita
    SIXTHS = (('1', 'Primo Tempo'), ('2', 'Secondo Tempo'), ('3', 'Terzo Tempo'), ('4', 'Quarto Tempo'), ('5', 'Quinto Tempo'), ('6', 'Sesto Tempo'), ('7', 'Supplementare'))
    COLORS = (
        ('Black', 'Nero'),
        ('Silver', 'Argento'),
        ('Gray', 'Grigio'),
        ('White', 'Bianco'),
        ('Maroon', 'Amaranto'),
        ('Red', 'Rosso'),
        ('Orange', 'Arancione'),
        ('Purple', 'Viola'),
        ('Fuchsia', 'Fucsia'),
        ('Green', 'Verde Scuro'),
        ('Lime', ' Verde Lime'),
        ('Yellow', 'Giallo'),
        ('Navy', 'Blue Navy'),
        ('Blue', 'Blu'),
        ('Teal', 'Verde Acqua'),
        ('Azure', 'Azzurro'),
        ('Pink', 'Rosa'))
    round = models.ForeignKey(Round, on_delete=models.CASCADE, blank=True, related_name='matches')
    team_A = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name='matches_A')
    points_A = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    team_B = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name='matches_B')
    points_B = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    time = models.ForeignKey('Time', on_delete=models.SET_NULL, blank=True, null=True, related_name='matches')
    court = models.ForeignKey('Court', on_delete=models.SET_NULL, blank=True, null=True, related_name='matches')
    number = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    sb_current_sixth = models.CharField(max_length=16, choices=SIXTHS, blank=True)
    sb_timer = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    sb_partial_A = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    sb_partial_B = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    sb_1_sixth_A = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    sb_1_sixth_B = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    sb_2_sixth_A = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    sb_2_sixth_B = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    sb_3_sixth_A = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    sb_3_sixth_B = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    sb_4_sixth_A = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    sb_4_sixth_B = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    sb_5_sixth_A = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    sb_5_sixth_B = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    sb_6_sixth_A = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    sb_6_sixth_B = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    sb_7_sixth_A = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    sb_7_sixth_B = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    sb_color_A = models.CharField(max_length=16, choices=COLORS, blank=True)
    sb_color_B = models.CharField(max_length=16, choices=COLORS, blank=True)

    def save(self, *args, **kwargs):
        if not self.sb_color_A:
            self.sb_color_A = self.team_A.color
        if not self.sb_color_B:
            self.sb_color_B = self.team_B.color
        super(Match, self).save(*args, **kwargs)

    def __str__(self):
        ptA = str(self.points_A) if self.points_A else ''
        ptB = str(self.points_B) if self.points_B else ''
        return str(self.team_A) + ' ' + ptA + ' - ' + ptB + ' ' + str(self.team_B)


class Score(models.Model):  # Punteggio
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='scores')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, related_name='scores')
    score = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True, default=0)
    games_played = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True, default=0)
    wins = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True, default=0)
    losses = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True, default=0)
    points_made = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True, default=0)
    points_conceded = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True, default=0)
    goals_made = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True, default=0)
    goals_conceded = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True, default=0)

    def __str__(self):
        return str(self.group) + ': ' + str(self.team) + ' -> ' + str(self.score)


class Court(models.Model):   # Campo
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True, related_name='courts')
    name = models.CharField(max_length=16, blank=True)
    importance = models.IntegerField(validators=[MinValueValidator(0)], blank=True, default=0)

    def __str__(self):
        return self.name


class Day(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True, related_name='days')
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Time(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE, null=True, related_name='times')
    time = models.CharField(max_length=16, blank=True)
    event = models.CharField(max_length=32, blank=True)  # se non ci sono partite
    precedent_time = models.OneToOneField('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='next_time')
    initial = models.BooleanField(default=False)

    def __str__(self):
        return self.time
