from django.db import models

class Summary(models.Model):
	row0 = models.FloatField()
	row1 = models.FloatField()
	row2 = models.FloatField()
	row3 = models.FloatField()
	row4 = models.FloatField()
	row5 = models.FloatField()
	row6= models.FloatField()
	row7= models.FloatField()
	row8= models.FloatField()
	row9= models.FloatField()
	row10= models.FloatField()
	row11= models.FloatField()
	row12= models.FloatField()
	row13= models.FloatField()
	row14= models.FloatField()
	row15= models.FloatField()
	row16= models.FloatField()
	row17= models.FloatField()
	row18= models.FloatField()
	row19= models.FloatField()
	row20= models.FloatField()
	row21= models.FloatField()
	row22= models.FloatField()
	row23= models.FloatField()
	row24= models.FloatField()
	parametro= models.CharField(max_length=128)
	fase= models.CharField(max_length=128)
	algoritmo= models.CharField(max_length=128)
	grupo= models.CharField(max_length=128)

	

class Result (models.Model):
	row0 = models.FloatField()
	row1 = models.FloatField()
	row2 = models.FloatField()
	row3 = models.FloatField()
	row4 = models.FloatField()
	row5 = models.FloatField()
	row6= models.FloatField()
	row7= models.FloatField()
	row8= models.FloatField()
	row9= models.FloatField()
	row10= models.FloatField()
	row11= models.FloatField()
	row12= models.FloatField()
	row13= models.FloatField()
	row14= models.FloatField()
	row15= models.FloatField()
	row16= models.FloatField()
	row17= models.FloatField()
	row18= models.FloatField()
	row19= models.FloatField()
	row20= models.FloatField()
	row21= models.FloatField()
	row22= models.FloatField()
	row23= models.FloatField()
	row24= models.FloatField()
	parametro= models.CharField(max_length=128)
	fase= models.CharField(max_length=128)
	algoritmo= models.CharField(max_length=128)
	cluster= models.CharField(max_length=128)
	etiqueta= models.CharField(max_length=128)
	flight = models.CharField(max_length=128)

class Labels (models.Model):
	VRTG = models.CharField(max_length=128)
	AOAC = models.CharField(max_length=128)
	FLAP = models.CharField(max_length=128)
	PTCH = models.CharField(max_length=128)
	ROLL = models.CharField(max_length=128)
	fase = models.CharField(max_length=128)
	flight = models.CharField(max_length=128)
	algoritmo = models.CharField(max_length=128)