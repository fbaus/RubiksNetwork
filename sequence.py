# SEQUENZA ORDINATA 
# RANDOM WALK con vincolo su livello
# MONTE-CARLO con vincolo sul livello
# ottenere una mappa completa entro un certo raggio dall'origine per vedere se c e un trend nel percorso piu breve.

import numpy as np
import cube as cu

S=['I', 'F', 'R', 'B', 'L', 'U', 'D']		#sequenza operazioni
C=cu.cubegen()	#crea configurazione iniziale
E=[]		#definisce lista edge
N=[ [[S[0]],C] ]	#definisce lista nodi con nodo iniziale 

#OPERAZIONI SEQUENZA PER LIVELLI
for i in range(1,len(S)):		#Esplora il primo livello tramite le 6 operazioni...
	L1=cu.rotate(C,S[i])		#...ruota la configurazione...
	N.append([[S[i]],L1])		#...crea l'elemento node come sequenza e configurazione...
	E.append([[S[0]],[S[i]]])		#...crea l'elemento edge come sequenza iniziale e sequenza finale.

	for k in range(1,len(S)):	#Esplora il secondo livello tramite 5 operazioni...
		if (S[k]!=S[i]):	#...infatti si usa questa condizione per evitare di tornare indietro...
			L2=cu.rotate(L1,S[k])			#...ruota la configurazione...
			N.append([[S[i],S[k]],L2 ])		#...crea l'elemento node come sequenza e configurazione...
			E.append([[S[i]],[S[i],S[k]]])	#...crea l'elemento edge come sequenza iniziale e sequenza finale.

			for h in range(1,len(S)):	#Esplora il terzo livello tramite 5 operazioni...
				if (S[h]!=S[k]):	#...infatti si usa questa condizione per evitare di tornare indietro...
					L3=cu.rotate(L2,S[h])				#...ruota la configurazione...
					N.append([[S[i],S[k],S[h]],L3])		#...crea l'elemento node come sequenza e configurazione...
					E.append([[S[i],S[k]],[S[i],S[k],S[h]]])	#...crea l'elemento edge come sequenza iniziale e sequenza finale.

# ORA, POSSONO ESSERCI NODI UGUALI OVVERO MODI DIVERSI DI ARRIVARE ALLA STESSA CONFIGURAZIONE. VOGLIAMO QUINDI RICONGIUNGERE QUESTI PUNTI.

#TROVA I ELEMENTI UGUALI NEL VETTORE NODI
D=[]						#Definisci la lista nera come vettore D...
for p in range(0,len(N)):			#...scorri tutti gli elementi di N e...
	for q in range(p+1,len(N)):		#...per ogni elemento successivo...
		if (N[p][1]==N[q][1]).all():	#...confronta i sotto-elementi configurazione dei due nodi in questione, se sono uguali...
			D.append([p,q])		#...crea un elemento nella lista nera dove [0] il copiato e [1] e' il copione.

#NELLA LISTA NERA CI POSSONO ESSERE DELLE RIDONDANZE CHE VOGLIAMO ELIMINARE PER NON FARE OPERAZIONI INUTILI. CONSIDERIAMO AD ESEMPIO CHE VI SIANO I SEGUENTI ELEMENTI:
#[1,7] , [1,18] , [1,44] ALLORA CI SARANNO ANCHE [7,18] , [7,44] , [18,44] CHE PERO' NON CI DICONO NIENTE IN PIU' E QUINDI VANNO ELIMINATI

#ELIMINA RIDONDANZE DALLA LISTA NERA (vedi pag14 per spiegazione)
for i in range(len(D)-1,0,-1): 		#Scorri la lista D al contrario sull'indice i (perche' elimineremo qualche elemento)...
	for j in range(i-1,-1,-1):		#...e per ogni elemento scorri tutti gli elementi precedenti nella lista sull'indice j...
		if(D[i].count(D[j][1])>0):	#...se almeno uno dei sotto-elementi di i e' presente come copione in j...
			del(D[i])		#...elimina i...
			break			#...e scorri all'elemento successivo perche' l'i-esimo non esiste piu'...
		else:				#...se non e' presente invece...
			continue		#...paragona i con il j successivo.

#Quando si trovano due nodi uguali uno dei due viene rimosso e il padre viene connesso col nodo che sopravvive. IL NODO RIMOSSO PUO' ANCHE AVERE DEI FIGLI E NIPOTI (UNA DISCENDENZA) E ANCHE LORO DEVONO ESSERE RIMOSSI. INFATTI DATO CHE USIAMO LE STESSE OPERAZIONI SUL COPIONE E SUL COPIATO SE QUESTI SONO UGUALI ALLORA ANCHE LE LORO DISCENDENZE SARANNO UGUALI. ALTRIMENTI CREANO DELLE RETI ISOLATE.


#ELIMINA DA N I COPIONI E LA LORO DISCENDENZA
for i in range(0,len(D)):					#Scorri la lista D e...
	Y=N[D[i][1]][0]
	for j in range(len(N)-1,-1,-1): 			#...scorri la lista nodi dal fondo...
		W=N[j][0][0:len(N[D[i][1]][0])]
#		while len(W)>len(Y):
#			Y.append(0)
#		while len(W)<len(Y):
#			W.append(0)	<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 'str' object has no attribute 'append': something strange must happen to create a string object instead of a list, and that is also why we have string nodes in the output file. Check all data type and remember that list are enclosed in [] while tuple are enclosed in ().
		if len(W)<len(Y):
			break
		k=0						#...se la sequenza del copione nell'elemento in D e' uguale alle prime operazioni... 
		for i in range(0,len(Y)-1):			#...della sequenza del nodo in questione...
			if W[i]==Y[i]:
				k=k+1
		if k==len(Y):
			N[j][1]='delete'			#...etichetta il nodo come "da eliminare". Cosi si eliminano anche le discendenze ma non gli avi.


	for j in range(len(E)-1,-1,-1): 			#...scorri la lista degli edges dal fondo...
		W=E[j][0][0:len(N[D[i][1]][0])]
#		while len(W)>len(Y):
#			Y.append(0)
#		while len(W)<len(Y):
#			W.append(0)    	<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 'str' object has no attribute 'append'
		if len(W)<len(Y):
			break
		k=0						#...se la sequenza del copione nell'elemento in D e' uguale alle prime operazioni... 
		for i in range(0,len(Y)-1):			#...della sequenza di partenza del edge in questione...
			if W[i]==Y[i]:
				k=k+1
		if k==len(Y):
			E[j][1]='delete'			#...etichetta l'edge come "da eliminare". Cosi si eliminano anche le discendenze ma non gli avi.
		W=E[j][1][0:len(N[D[i][1]][0])]
#		while len(W)<len(Y):
#			W.append(0)    	<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 'str' object has no attribute 'append'
		if len(W)<len(Y):
			break
		k=0						#...se la sequenza del copione nell'elemento in D e' uguale alle prime operazioni... 
		for i in range(0,len(Y)-1):			#...della sequenza di arrivo del edge in questione...
			if W[i]==Y[i]:
				k=k+1
		if k==len(Y):
			E[j][1]='delete'			#...etichetta l'edge come "da eliminare". Cosi si eliminano anche le discendenze ma non gli avi.


for i in range(len(N)-1,-1,-1): 				#...scorri la lista nodi dal fondo...
	if N[i][1]=='delete':					#...controlla se e' segnato come da eliminare...
		del(N[i])					#...se si elimina.

for i in range(len(E)-1,-1,-1): 				#...scorri la lista edge dal fondo...
	if E[i][1]=='delete':					#...controlla se e' segnato come da eliminare...
		del(E[i])					#...se si elimina.



#RICOLLEGA IL COPIATO CON IL PADRE DEL COPIONE
for i in range(0,len(D)):	#Scorri la lista D e...
	E.append([ N[ D[i][0] ][0] , N[D[i][1]][0] [0:len(N[D[i][1]][0])-1] ])	#...ricollega il copiato al padre del copione...


#DATA
from time import gmtime, strftime
dat=strftime("%Y-%m-%d_%H%M%S", gmtime())
#dat=dat.replace(' ','_')
#dat=dat.replace(':','')

#SCRIVI FILE
with open(dat+'.gexf', 'a') as the_file:
	the_file.write('<gexf>\n\t<meta lastmodifieddate="' +dat+ '">\n\t\t<creator>FB</creator>\n\t</meta>\n\t<graph defaultedgetype="undirected" idtype="string" type="static">\n\t\t<nodes count="' +str(len(N))+ '">\n')

for i in range(len(N)):
	with open(dat+'.gexf', 'a') as the_file:
		the_file.write('\t\t\t<node id="' +str(N[i][0])+ '" label="' +str(N[i][0])+ '"/>\n')

with open(dat+'.gexf', 'a') as the_file:
	the_file.write('\t\t</nodes>\n\t\t<edges count="' +str(len(E))+ '">\n')

for i in range(len(E)):
	with open(dat+'.gexf', 'a') as the_file:
		the_file.write('\t\t\t<edge id="' +str(i)+ '" source="' +str(E[i][0])+ '" target="'  +str(E[i][1])+  '" weight="1.0"/>\n')

with open(dat+'.gexf', 'a') as the_file:
	the_file.write('\t\t</edges>\n\t</graph>\n</gexf>')
