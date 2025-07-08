import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.anno1 = None
        self.anno2 = None

    def handleBuildGraph(self, e):
        self._view._txtGraphDetails.controls.clear()
        self._view.update_page()

        self._model.build_graph(self.anno1, self.anno2)

        self._view._txtGraphDetails.controls.append(ft.Text(self._model.grafo))

        self._view.update_page()


    def handlePrintDetails(self, e):
        self._view._txtGraphDetails.controls.clear()
        det = self._model.details()
        for d in det:
            self._view._txtGraphDetails.controls.append(ft.Text(f"{d[0]} - {d[1]}"))
        self._view.update_page()



    def handleCercaDreamChampionship(self, e):
        pass

    def fill_dropdownAnni(self):
        lista_opzioni = DAO.getter_anni()
        for o in lista_opzioni:
            self._view._ddYear1.options.append(ft.dropdown.Option(key= o,
                                                                  text=o,
                                                                  data= o,
                                                                  on_click=self.read_dropdownAnni1))
            self._view._ddYear2.options.append(ft.dropdown.Option(key=o,
                                                                  text=o,
                                                                  data=o,
                                                                  on_click=self.read_dropdownAnni2))
    def read_dropdownAnni1(self, e):
        self.anno1 = e.control.data
        print(f"valore letto: {self.anno1} - {type(self.anno1)}")

    def read_dropdownAnni2(self, e):
        self.anno2 = e.control.data
        print(f"valore letto: {self.anno2} - {type(self.anno2)}")
