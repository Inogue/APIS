#!/bin/python3

import time
import json
import requests
import sys
from fabulous import utils,image
from textual.app import App, ComposeResult
from textual.widgets import Button, Label
from textual.widget import Widget
import tkinter as tk
from PIL import Image, ImageTk

class Blackjack(App):
	CSS_PATH = "style.css"
	def compose(self) -> ComposeResult:
		yield Label("Blackjack", id="hello")
		M
		self.option_button1 = Button("Rules", id="rules")
		self.option_button2 = Button("Draw_card", id="card")
		self.close_button = Button("Close", id="close")
		self.rules = Label("1-El objetivo del juego es llegar a 21, quien mas cerca esté, gana.\n2-A la hora de sumar las cartas, se suman por su numero excepto el as y las figuras:\nEl AS puede contar como un 1 o como un 11 dependiendo de lo que decida el jugador, las figuras cuentan todas 10.\n3-El croupier se plantara en el momento que alcance la puntuacion de 16 o mas.\n4-Cuando al croupier le toca un as, siempre sera 11 a no ser que se pase de 21, entonces sera 1.\n5-Puedes pedir las cartas que quieras, cuando llegues a 22 o mas habras perdido.")
		yield self.option_button1
		yield self.option_button2	
		yield self.close_button

	def on_mount(self) -> None:
		self.screen.styles.background = "darkblue"
		self.close_button.styles.background = "red"
		self.option_button1.styles.background = "red"
		self.option_button2.styles.background = "red"

	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id=="close":
			self.exit(event.button.id)
		elif event.button.id=="rules":
			self.widgets.clear()
			rules()
		elif event.button.id=="card":
			self.widgets.clear()
			draw_card(deck_id, 1)
def new_deck():
	api_url="https://deckofcardsapi.com/api/deck/new/"

	response = requests.get(api_url)

	info = response.json()

	deck_id=info["deck_id"]
	return deck_id


def draw_card(deck_id, cards):
	
	api_url= "https://deckofcardsapi.com/api/deck/"+deck_id+"/draw/?count="+str(cards)

	response = requests.get(api_url)

	info = response.json()

	card=info["cards"][0]["image"]
	card_value=info["cards"][0]["value"]
	if card_value=="KING" or card_value=="QUEEN" or card_value=="JACK":
		card_value=10
	
	if card_value=="ACE":
		value=input("Que valor quieres que tenga tu as, 1 o 11?")
		if str(value)=="11":
			card_value=11
		elif str(value)=="1":
			card_value=1
		else:
			print("Valor incorrecto, te pondremos un 1")

	player_deck.append(card_value)
	
	images= requests.get(card).content

	image_name="carta.png"

	imagen = Image.open(image_name)
	imagen.thumbnail((500, 500))
	imagen = ImageTk.PhotoImage(imagen)
	etiqueta.configure(image=imagen)
	etiqueta.image = imagen
	ventana = tk.Tk()
	etiqueta = tk.Label(ventana)
	etiqueta.pack()
	abrir_imagen(image_name)
	ventana.mainloop()

	if cards > 1:
		card2=info["cards"][1]["image"]
		card_value2=info["cards"][1]["value"]
		if card_value2=="KING" or card_value2=="QUEEN" or card_value2=="JACK":
			card_value2=10
	
		if card_value2=="ACE":
			value2=input("Te ha tocado un as, que valor quieres que tenga? ¿1 o 11?")
		
			if str(value2)=="11":
				card_value2=11
			elif str(value2)=="1":
				card_value2=1
			else:
				print("Valor incorrecto, te pondremos un 1")
				card_value2=1
		player_deck.append(card_value2)

		images2= requests.get(card2).content
		image_name2="carta2.png"
		with open(image_name2, "wb") as handler:
			handler.write(images2)
			img2 = image.Image(image_name2)
			time.sleep(1)
			print(img2)

def croupier_draw_card(deck_id, cards):
	api_url= "https://deckofcardsapi.com/api/deck/"+deck_id+"/draw/?count="+str(cards)
	response = requests.get(api_url)
	info = response.json()
	card=info["cards"][0]["image"]
	card_value=info["cards"][0]["value"]

	if card_value=="KING" or card_value=="QUEEN" or card_value=="JACK":
		card_value=10
	if card_value=="ACE":
		card_value=11
	croupier_deck.append(card_value)

	images= requests.get(card).content
	image_name="croupier_card.png"

	with open(image_name, "wb") as handler:
		handler.write(images)
		img = image.Image(image_name)
		time.sleep(1)
		print(img)
	
	if cards > 1:
		card2=info["cards"][1]["image"]
		card_value2=info["cards"][1]["value"]

		if card_value2=="KING" or card_value2=="QUEEN" or card_value2=="JACK":
			card_value2=10
		if card_value2=="ACE":
			if card_value==11:
				card_value2=1
			card_value2=11
		croupier_deck.append(card_value2)

		images2= requests.get(card2).content
		image_name2="croupier_card2.png"
		
		with open(image_name2, "wb") as handler:
			handler.write(images2)
			img2 = image.Image(image_name2)
			time.sleep(1)
			print(img2)

def shuffle_cards(deck_id):
	api_url="https://deckofcardsapi.com/api/deck/"+deck_id+"/shuffle/"
	
	response = requests.get(api_url)
	
	info = response.json()
	 
def count(sum_num, sum_num2, final_count):
	
	for num in player_deck:
		sum_num += int(num) 
	print("Esta es tu suma: "+str(sum_num))
	print("")

	for num in croupier_deck:
		sum_num2 += int(num)

	
	if int(sum_num2)>=16:
		print("Esta es la suma del croupier: "+str(sum_num2))
		print("")
		print("El croupier se planta")
		print("")
		if final_count==True:
			victory(sum_num, sum_num2)
		return "stop"
	else:
		print("Esta es la suma del croupier: "+str(sum_num2))
		print("")
	if final_count==True:
		victory(sum_num, sum_num2)

def victory(sum_num, sum_num2):
	if sum_num>21:
		print("Has perdido, el croupier gana")
	elif sum_num2>21:
		print("El croupier ha perdido, tu ganas")
	elif sum_num>sum_num2:
		print("Has ganado, el croupier pierde")
	elif sum_num<sum_num2:
		print("El croupier ha ganado, tu pierdes")
	elif sum_num==sum_num2:
		print("Empate")
	for i in range(len(player_deck)):
		player_deck.pop()
	for i in range(len(croupier_deck)):
		croupier_deck.pop()

def rules():
	Label("1-El objetivo del juego es llegar a 21, quien mas cerca esté, gana.\n2-A la hora de sumar las cartas, se suman por su numero excepto el as y las figuras:\nEl AS puede contar como un 1 o como un 11 dependiendo de lo que decida el jugador, la    s figuras cuentan todas 10.\n3-El croupier se plantara en el momento que alcance la puntuacion de 16 o mas.\n4-Cuando al croupier le toca un as, siempre sera 11 a no ser que se pase de 21, entonces sera 1.\n5-Puedes pedir las cartas que quieras, cuando llegues a 22 o     mas habras perdido.")	

def game():
	opc=False
	
	while not opc:
		print("Pues comencemos")
		print(deck_id)
		print("")
		shuffle_cards(deck_id)
		print("Estas son tus cartas")
		draw_card(deck_id,2)
		print(player_deck)
		print("Estas son las cartas del croupier")
		croupier_draw_card(deck_id,2)
		print("Tus cartas"+str(player_deck))
		print("Cartas del croupier"+str(croupier_deck))
		print("")
		count(sum_num,sum_num2, False)
		opcion=	input("Quieres sacar otra carta?(Y/n)" )
		while opcion!="n":
			if opcion.lower()=="y":
				draw_card(deck_id,1)
				print(player_deck)
			else:
				break
			opcion= input("Quieres sacar otra carta?(Y/n)" )
		ok=count(sum_num, sum_num2, False)
		while ok!= "stop":
			if ok=="stop":
				break
			else:
				print("El croupier saca otra carta")
				print("")
				croupier_draw_card(deck_id, 1)
				print(croupier_deck)
			ok=count(sum_num, sum_num2, False)
		time.sleep(1)
		print("RECUENTO FINAL")
		print("-------------")
		count(sum_num, sum_num2, True)
		print("")
		break


if __name__ == "__main__":
	app = Blackjack()
	app.run()
	deck_id=new_deck()
	sum_num=0
	sum_num2=0
	player_deck=[]
	croupier_deck=[]
	print("Bienvenido a la partida de blackjack")
	salida=""

	while salida!="s":
		opc= input("Quieres comenzar la partida o salir?(Y/s)")
		if opc.lower() == "s":
			print("Esta bien, adios")
			break
		opc2=input("Quieres ver las reglas?(Y/n)")
		if opc2.lower()=="y":
			rules()
			time.sleep(20)
			print("")
		else:
			print("Si no quieres leer las reglas, el juego comienza")
		game()




