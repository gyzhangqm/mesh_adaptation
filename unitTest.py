a = SpringSystem()

a.addNode(nodePosition=[0.,0.], nodeType=Locked)
a.addNode(nodePosition=[0.,2.], nodeType=Locked)
a.addnode(nodeposition=[1.,0.5], nodeType=Inner)
a.addNode(nodePosition=[1.,3.], nodeType=Locked)

a.addSpring(nodes=[0,2], springStiffness=1.)
a.addSpring(nodes=[1,2], springStiffness=1.)
a.addSpring(nodes=[3,2], springStiffness=1.)

a.solveSystem(tolerance=1e-4, relaxation=0.2)

check_close(a.getNode(2).position == [1.,1.], 1e-3)

#####

a = SpringSystem()

a.addNode(nodePosition=[0.,0.], nodeType=Boundary, boundaryNormal=[0.,1.])
a.addNode(nodePosition=[0.,2.], nodeType=Boundary, boundaryNormal=[0.,1.])
a.addnode(nodeposition=[1.,.5], nodeType=Inner)
a.addNode(nodePosition=[1.,3.], nodeType=Locked)

a.addSpring(nodes=[0,2], springStiffness=1.)
a.addSpring(nodes=[1,2], springStiffness=1.)
a.addSpring(nodes=[3,2], springStiffness=1.)

a.solveSystem(tolerance=1e-4, relaxation=0.2)

check_close(a.getNode(0).position == [0.,1.], 1e-3)
check_close(a.getNode(1).position == [0.,1.], 1e-3)
check_close(a.getNode(2).position == [1.,1.], 1e-3)
