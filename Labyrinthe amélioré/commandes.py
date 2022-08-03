from tkinter import *


def c1():
    Frame1.destroy()
    Frame2.destroy()
    Frame3.destroy()
    Frame4= Frame(Mafenetre, bg='white', borderwidth=2)
    Frame4.pack(side=LEFT, padx=10, pady=10)
    label=Label(Frame4, text='test')
    label.pack(padx=10, pady=10)
    Button(Frame4, text='Effacer', bg='blue', command=Frame4.destroy).pack(padx=10, pady=10)


# Création de la fenêtre principale
Mafenetre = Tk()
Mafenetre.title('Frame widget')
Mafenetre['bg']='bisque' # couleur de fond

# création d'un widget Frame dans la fenêtre principale
Frame1 = Frame(Mafenetre,borderwidth=2,relief=GROOVE)
Frame1.pack(side=LEFT,padx=10,pady=10)

# création d'un second widget Frame dans la fenêtre principale
Frame2 = Frame(Mafenetre,borderwidth=2,relief=GROOVE)
Frame2.pack(side=LEFT,padx=10,pady=10)

# création d'un widget Frame... dans un widget Frame
# le widget Frame1 est le parent du widget Frame3
# le parent du widget Frame1 est le widget Mafenetre (fenêtre principale)
Frame3 = Frame(Frame1,bg="white",borderwidth=2,relief=GROOVE)
Frame3.pack(side=LEFT,padx=10,pady=10)

# création d'un widget Label et d'un widget Button dans un widget Frame
Label(Frame1,text="RDV dentiste samedi à 15h").pack(padx=10,pady=10)
Button(Frame1,text="Effacer",fg='navy',command=c1).pack(padx=10,pady=10)

Label(Frame2,text="Réviser le contrôle d'info").pack(padx=10,pady=10)
Button(Frame2,text="Effacer",fg='navy',command=Frame2.destroy).pack(padx=10,pady=10)

Label(Frame3,text="RDV dentiste à 10h",bg="white").pack(padx=10,pady=10)
Button(Frame3,text="Effacer",fg='navy',command=Frame3.destroy).pack(padx=10,pady=10)

Mafenetre.mainloop()



