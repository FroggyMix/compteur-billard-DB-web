import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import simplejson
#from gestionnaire.frame_state import frame_states
from gestionnaire.models import *
#from datetime import datetime
from django.utils import timezone


#from channels import Group



class FrameConsumer_sync(WebsocketConsumer):
	def connect(self):
		self.frame_id=self.scope['url_route']['kwargs']['frame_id'] #récupération de l'ide de la frame
		self.frame_group_name = 'frame_%s' %self.frame_id #création d'un groupe pour les permettre les clients multiples sur une même frame
		#On rejoint le groupe
		async_to_sync(self.channel_layer.group_add)(
			self.frame_group_name,
			self.channel_name
		)
		print('connection établie pour la frame {} sur le groupe_name {} et la channel {}' .format(self.frame_id, self.frame_group_name, self.channel_name))
		self.accept()
		#On envoie tout de suite l'état de la frame
		async_to_sync(self.channel_layer.group_send)(self.frame_group_name,{'type': 'score_message','message':Frame.objects.get(pk=self.frame_id).frame_states()})


	def disconnect(self, close_code):
		async_to_sync(self.channel_layer.group_discard)(
			self.frame_group_name,
			self.channel_name,
		)

	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		print("[{}]<<<<<<<<<<RECEPTION MESSAGE: {}".format(timezone.localtime(timezone.now()),text_data_json['action']))
		if text_data_json['action'] == 'correction':
			j1_add = text_data_json['j1_add']
			j2_add = text_data_json['j2_add']
			reprise_add = text_data_json['reprise_add'] 
			print('correction = ({}, {}, {})'.format(j1_add,j2_add,reprise_add))
			if j1_add != "" and j1_add != 0:
				Frame.objects.get(pk=self.frame_id).correction_score(1,j1_add)
			if j2_add != "" and j1_add != 0:
				Frame.objects.get(pk=self.frame_id).correction_score(2,j2_add)
			if reprise_add != "" and reprise_add != 0:
				Frame.objects.get(pk=self.frame_id).correction_score(0,reprise_add)

		if text_data_json['action'] == 'score':
			Frame.objects.get(pk=self.frame_id).ajoute_evt('score',text_data_json['joueur'],text_data_json['points'])
		elif text_data_json['action'] == 'pass':
			#la main passe et éventuellement on incrémente
			Frame.objects.get(pk=self.frame_id).ajoute_evt('pass',text_data_json['joueur'])		
		elif text_data_json['action'] == 'toss':
			#Le toss a décidé du joueur qui commence : on le log dans les evt et date le debut de la frame (voire du match)
			Frame.objects.get(pk=self.frame_id).ajoute_evt('toss-engage',text_data_json['joueur'])
		elif text_data_json['action'] == 'start':
			#dans le cas où frame.num>1 le joueur vient d'engager
			Frame.objects.get(pk=self.frame_id).ajoute_evt('engage',text_data_json['joueur'])
		elif text_data_json['action'] == 'annuler_action':
			#Demande d'annulation du dernier coup
			Frame.objects.get(pk=self.frame_id).undo_last_event()
		elif text_data_json['action'] == 'concede':
			#Le joueur actif concede la frame
			Frame.objects.get(pk=self.frame_id).ajoute_evt('concedeF',text_data_json['joueur'])
		elif text_data_json['action'] == 'chrono-pause':
			#L'arbitre a mis le jeu en pause
			Frame.objects.get(pk=self.frame_id).ajoute_evt('chrono-pause')
		elif text_data_json['action'] == 'chrono-play':
			#L'arbitre a remis le jeu en route
			Frame.objects.get(pk=self.frame_id).ajoute_evt('chrono-play')
		#Après avoir traité les diff type d'evt, on envoi un signal de maj , sauf si on est dans un cas de redirection	
		if text_data_json['action'] == 'redirect':
			#demande de changement d'url (frame suivante ou retour frame_liste
			async_to_sync(self.channel_layer.group_send)(self.frame_group_name,{'type': 'redirect','message':{'url':text_data_json['url']}})
		else:	
			#On met à jour tous les scoreboards qui suivent cette frame
			async_to_sync(self.channel_layer.group_send)(self.frame_group_name,{'type': 'score_message','message':Frame.objects.get(pk=self.frame_id).frame_states()})

	def score_message(self,event):
		message = event['message']
		print("[{}]>>>>>>>>>EMISSION MESSAGE ".format(timezone.localtime(timezone.now())))
		self.send(text_data=json.dumps({'message':message}))
	
	def redirect(self,event):
		message = event['message']
		self.send(text_data=json.dumps({'message':message}))


class FrameConsumer_async(AsyncWebsocketConsumer):
	async def connect(self):
		self.frame_id=self.scope['url_route']['kwargs']['frame_id'] #récupération de l'ide de la frame
		self.frame_group_name = 'frame_%s' %self.frame_id #création d'un groupe pour les permettre les clients multiples sur une même frame
		#On rejoint le groupe
		await self.channel_layer.group_add(
			self.frame_group_name,
			self.channel_name
		)
		print('connection établie pour la frame {} sur le groupe_name {} et la channel {}' .format(self.frame_id, self.frame_group_name, self.channel_name))
		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.frame_group_name,
			self.channel_name,
		)

	async def receive(self, text_data):
		# data_json=json.loads(text_data)
		# j1_add=data_json['j1_add']
		# j2_add=data_json['j2_add']
		
		#test envoi le channel name à la table
		

		await self.channel_layer.group_send('frame_2',{'messager': 'blabla'})
		# Group(self.frame_group_name).send({'message': 'test'})
