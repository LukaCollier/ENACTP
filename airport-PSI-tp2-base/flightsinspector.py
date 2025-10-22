from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
import radar_view
import timestep
class Flighsinspector(QWidget):
    def __init__(self,radar):
        super().__init__()
        self.radar=radar
        uic.loadUi("flightsinspector.ui",self)
        radar.flight_selected.connect(self.modif)
    def modif(self,f):
        call_sign=f.call_sign
        mvt=f.type.name
        wvc=f.cat.name
        stand=f.stand.name
        runway=f.runway.name
        qfu=f.qfu
        time=timestep.to_hms(f.start_t)
        self.Callsign_Data.setText(call_sign)
        self.Movement_Type_Data.setText(mvt)
        self.Wake_Vortex_Category_Data.setText(wvc)
        self.Used_Stand_Data.setText(stand)
        self.Used_Runway_Data.setText(runway)
        self.Used_QFU_Data.setText(qfu)
        self.Beginning_time_Data.setText(time)
        self.CFMU_slot_Data.setText(str(f.slot))