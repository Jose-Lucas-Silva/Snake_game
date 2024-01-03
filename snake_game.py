import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

#variaveis
largura = 625
altura = 350

x_lagarta = largura /2
y_lagarta = altura /2

velocidade = 1
x_controle = velocidade
y_controle = 0

x_maca = randint(60,583)
y_maca = randint(70,298)

x_obst1 = randint(60, 583)
y_obst1 = randint(70, 298)
x_obst2 = randint(60, 583)
y_obst2 = randint(70, 298)

fonte = pygame.font.SysFont('gabriola', 40, True, False)

pontos = 0
recorde = 0

lista_lagarta = []
compr_inicial = 20
morreu = False

#tela
tela = pygame.display.set_mode((largura,altura))
pygame.display.set_caption('Snake Game')

#Sons do jogo
pygame.mixer.music.set_volume(0.1)
musica_de_Fundo = pygame.mixer.music.load('musicajogo.mid')
pygame.mixer.music.play(-1,0,0)
som_Colisao = pygame.mixer.Sound('som_comendo.wav')

def limitar_tamanhoI(lista_lagarta):
    for XeY in lista_lagarta:
        pygame.draw.rect(tela, (176,224,230), (XeY[0], XeY[1], 20, 20))
        if len(lista_lagarta) > compr_inicial:
            del lista_lagarta[0]

def morte_tela():
    if morreu == True:
        fonteM = pygame.font.SysFont('gabriola', 35, True, False)
        mensagem3 = fonteM.render('você morreu! para recomeçar pressione R', True, (0, 0, 0))
        ret_texto = mensagem3.get_rect()
        while morreu:
            tela.fill((85, 107, 47))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        reiniciar_jogo()
            ret_texto.center = (largura // 2, altura // 2)
            tela.blit(mensagem3, ret_texto)
            pygame.display.update()

def reiniciar_jogo():
    global pontos,compr_inicial,x_lagarta,y_lagarta,lista_lagarta,lista_cabeca,x_maca,y_maca,morreu
    pontos = 0
    compr_inicial = 20
    x_lagarta = largura /2
    y_lagarta = altura /2
    lista_lagarta = []
    lista_cabeca= []
    x_maca = randint(60, 583)
    y_maca = randint(70, 298)
    morreu = False

#loop do jogo
loop_jogo = True
while loop_jogo:
    pygame.time.Clock().tick(300)#frames do jogo
    mensagem1 = fonte.render(f'Pontos:{pontos}', False, (0,0,0), (85,107,47))#mensagem na tela
    mensagem2 = fonte.render(f'Recorde:{recorde}', False, (0,0,0), (85,107,47))# mensagem na tela
    tela.fill((85,107,47))
    for event in pygame.event.get():
        # sair do jogo pelo (X)
        if event.type == QUIT:
            pygame.quit()
            exit()

    #mover cobra
        if event.type == KEYDOWN:
            if event.key == K_a:
                if x_controle == velocidade:
                    pass
                else:
                    x_controle = -velocidade
                    y_controle = 0
            if event.key == K_d:
                if x_controle == -velocidade:
                    pass
                else:
                    x_controle = velocidade
                    y_controle = 0
            if event.key == K_w:
                if y_controle == velocidade:
                    pass
                else:
                    x_controle = 0
                    y_controle = -velocidade
            if event.key == K_s:
                if y_controle == -velocidade:
                    pass
                else:
                    x_controle = 0
                    y_controle = velocidade

    x_lagarta = x_lagarta + x_controle
    y_lagarta = y_lagarta + y_controle

    #linhas de limitação da tela
    lateral1 = pygame.draw.line(tela, (0,0,0), (1,50), (624,50))
    lateral2 = pygame.draw.line(tela, (0,0,0), (1,349), (624,349))
    lateral3 = pygame.draw.line(tela, (0,0,0), (1,1), (1,349))
    lateral4 = pygame.draw.line(tela, (0,0,0), (624,1), (624,349))

    #cobra
    lagarta = pygame.draw.rect(tela, (176,224,230), (x_lagarta,y_lagarta,20,20))
    lista_cabeca = []
    lista_cabeca.append(x_lagarta)
    lista_cabeca.append(y_lagarta)
    lista_lagarta.append(lista_cabeca)
    limitar_tamanhoI(lista_lagarta)

    #Maçã
    maca = pygame.draw.rect(tela, (255,0,0), (x_maca,y_maca,20,20))

    #obstaculo
    obstaculo1 = pygame.draw.rect(tela, (0, 0, 0), (x_obst1, y_obst1, 20, 20))
    y_obst1 += 1
    if y_obst1 == 350:
        x_obst1 = randint(60, 583)
        y_obst1 = randint(40, 40)
    obstaculo2 = pygame.draw.rect(tela, (0, 0, 0), (x_obst2, y_obst2, 20, 20))
    x_obst2 += 1
    if x_obst2 == 625:
        x_obst2 = randint(0, 0)
        y_obst2 = randint(70, 298)
    #Colisão com maçã
    if lagarta.colliderect(maca):
        x_maca = randint(60,583)
        y_maca = randint(70,298)
        pontos += 1
        som_Colisao.play()
        compr_inicial = compr_inicial + 10

    #colisão com obstaculo
    if lagarta.colliderect(obstaculo1):
        if pontos > recorde:
            recorde = pontos
        morreu = True
        morte_tela()
    if lagarta.colliderect(obstaculo2):
        if pontos > recorde:
            recorde = pontos
        morreu = True
        morte_tela()

    #colisão com corpo
    if lista_lagarta.count(lista_cabeca) > 1:
        if pontos > recorde:
            recorde = pontos
        morreu = True
        morte_tela()

    #colisão com parede
    if x_lagarta > largura:
        if pontos > recorde:
            recorde = pontos
        morreu = True
        morte_tela()
    if x_lagarta < 0:
        if pontos > recorde:
            recorde = pontos
        morreu = True
        morte_tela()
    if y_lagarta < 40:
        if pontos > recorde:
            recorde = pontos
        morreu = True
        morte_tela()
    if y_lagarta > altura:
        if pontos > recorde:
            recorde = pontos
        morreu = True
        morte_tela()

    tela.blit(mensagem1, (20,10))
    tela.blit(mensagem2, (450, 10))
    pygame.display.flip()