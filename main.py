from controllers.Controller import Controller
from models.Database import Database
from models.Model import Model
from views.View import View

if __name__ == '__main__':
    db = Database()
    model = Model(db)
    view = View(model)
    Controller(model, view)

    view.mainloop() # Koodi "viimane" rida