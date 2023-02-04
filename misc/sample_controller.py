class blockmesh_layout_controller:
    """This is a sample controller that implements 2:1 multiplexer logic 
    where the output method return methods based upon input message: type"""
    
    def __init__(self, type):
        self.type = type
        self.ret_mapper = {"Recents": "draw_func1",
                           "Design": "draw_func2"}
        
    def output(self):
        getattr(self, self.ret_mapper[self.type])()
        
    def draw_func1(self):
        print("This is draw Function 1")
    
    def draw_func2(self):
        print("This is draw Function 2")
        
getattr(blockmesh_layout_controller("Design"), "output")()