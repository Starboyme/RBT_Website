from vpython import *
#GlowScript 3.0 VPython
rad=3.141459/180
scene = canvas(title='Red-Black Trees ', width=1200,   height=600,  center=vector(0,0,0), background=color.white)
vertex=[]
leftedge=[]
rightedge=[]
lb=[]
fnd=box(pos=vector(20,20,0), axis=vector(0,0,0), size=vector(8,4,0.05), color=color.white,visible=False)
unfnd=box(pos=vector(30,20,0), axis=vector(0,0,0), size=vector(8,4,0.05), color=color.white,visible=False)
l1=label(pos=fnd.pos,text="found",color=color.black,opacity=0, height=15, space=15, box=False, visible=False )
l2=label(pos=unfnd.pos,text="not found",color=color.black,opacity=0, height=15, space=15, box=False, visible=False)
# data structure that represents a node in the tree
class Node():
    def __init__(self, data):
        self.data = data  # holds the key
        self.parent = None #pointer to the parent
        self.left = None # pointer to left child
        self.right = None #pointer to right child
        self.color = 1 # 1 . Red, 0 . Black



class RedBlackTree():
    def __init__(self):
        self.TNULL = Node(0)
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL


    def __search_tree_helper(self, node, key):
        if node == self.TNULL or key == node.data:
            return node

        if key < node.data:
            return self.__search_tree_helper(node.left, key)
        return self.__search_tree_helper(node.right, key)

    # fix the rb tree modified by the operation
    def __fix_delete(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    # case 3.1
                    s.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    # case 3.2
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        # case 3.3
                        s.left.color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right

                    # case 3.4
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    # case 3.1
                    s.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.left.color == 0 and s.right.color == 0:
                    # case 3.2
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        # case 3.3
                        s.right.color = 0
                        s.colors = x.parent.left 

                    # case 3.4
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 0

    def __rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def remove_node(self,key):
        # find the node containing key
        node=self.root
        z = self.TNULL
        while node != self.TNULL:
            if node.data == key:
                z = node

            if node.data <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            print("Couldn't find key in the tree")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif (z.right == self.TNULL):
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:
            self.__fix_delete(x)
    
    # fix the red-black tree
    def  __fix_insert(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left # uncle
                if u.color == 1:
                    # case 3.1
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        # case 3.2.2
                        k = k.parent
                        self.right_rotate(k)
                    # case 3.2.1
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right # uncle

                if u.color == 1:
                    # mirror case 3.1
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent 
                else:
                    if k == k.parent.right:
                        # mirror case 3.2.2
                        k = k.parent
                        self.left_rotate(k)
                    # mirror case 3.2.1
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    def __print_helper(self, node, indent, last):
        # print the tree structure on the screen
        if node != self.TNULL:
            print(indent,end='')
            if last:
                print("R----",end='')
                indent += "     "
            else:
                print("L----",end='')
                indent += "|    "

            s_color = "RED" if node.color == 1 else "BLACK"
            print(str(node.data) + "(" + s_color + ")")
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)
    
    # search the tree for the key k
    # and return the corresponding node
    def searchTree(self, k):
        return self.__search_tree_helper(self.root, k)

    # find the node with the minimum key
    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # rotate right at node x
    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # insert the key to the tree in its appropriate position
    # and fix the tree
    def insert(self, key):
        # Ordinary Binary Search Insertion
        node = Node(key)
    
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1 # new node must be red

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        # y is parent of x
        node.parent = y
        if y == None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        # if new node is a root node, simply return
        if node.parent == None:
            node.color = 0
            return

        # if the grandparent is None, simply return
        if node.parent.parent == None:
            return

        # Fix the tree
        self.__fix_insert(node)

    # print the tree structure on the screen
    def pretty_print(self):
        self.__print_helper(self.root, "", True)
    
    def printLevelOrder(self):
        root=self.root
        if(root is None):
            return
        queue=[]
        temp=[]
        j=0
        queue.append(root)
        while(len(queue)>0):
            temp.append([])
            count=len(queue)
            while(count>0):
                node=queue.pop(0)
                temp[j].append(node)
                if(node.left is not None):
                    queue.append(node.left)
                if(node.right is not None):
                    queue.append(node.right)
                count-=1
            j+=1
        return temp
def visual(tree,search,res):
    fnd.color=color.white
    unfnd.color=color.white
    fnd.visible=False
    unfnd.visible=False
    l1.visible=False
    l2.visible=False
    if(len(vertex)!=0):
        while(len(vertex)>0):
            vertex[0].visible=False
            s=vertex.pop(0)
            del s
    if(len(leftedge)!=0):
        while(len(leftedge)>0):
            leftedge[0].visible=False
            s=leftedge.pop(0)
            del s
    if(len(rightedge)!=0):
        while(len(rightedge)>0):
            rightedge[0].visible=False
            s=rightedge.pop(0)
            del s
    if(len(lb)!=0):
        while(len(lb)>0):
            lb[0].visible=False
            s=lb.pop(0)
            del s
    dict[0]=color.black
    dict[1]=color.red
    num=0
    ln=len(tree)
    l=32
    r=8
    j=0
    temp=[]
    child=[]
    grp={}
    val={}
    while(num<ln):
        if(num==0 and tree[0][0].data!=0):
            vertex[j]=sphere(pos=vector(0,10,0),radius=r,color=dict[tree[0][0].color])
            lb[j]=label(pos=vertex[j].pos,text=tree[0][0].data,color=color.white,opacity=0, height=r*4+4, space=r*4+4, box=False)
            val[j]=tree[0][0].data
            leftedge[j]=arrow(pos=vector(0,10,0),axis=vector(vertex[j].pos.x+(l*cos(-150*rad)),vertex[j].pos.y+(l*sin(-150*rad)),0),shaftwidth=0.5,headwidth=0.2,color=color.black)
            rightedge[j]=arrow(pos=vector(0,10,0),axis=vector(vertex[j].pos.x+(l*cos(-30*rad)),vertex[j].pos.y+(l*sin(-30*rad)),0),shaftwidth=0.5,headwidth=0.2,color=color.black)
            temp.append(leftedge[j])
            temp.append(rightedge[j])
            child.append(j)
            child.append(j)
            j+=1
        else:
            k=0
            for i in range(len(tree[num])):
                xxx=tree[num][i].data
                if(xxx!=0):
                    vertex[j]=sphere(pos=temp[k].axis+temp[k].pos,radius=r,color=dict[tree[num][i].color])
                    if(child[0] not in grp):
                        grp[child[0]]=[j]
                    else:
                        grp[child[0]].append(j)
                    lb[j]=label(pos=vertex[j].pos,text=tree[num][i].data,color=color.white,opacity=0, space=r*4, height=r*4, box=False)
                    val[j]=tree[num][i].data
                    leftedge[j]=arrow(pos=vertex[j].pos,axis=vector((l*cos(-150*rad)),(l*sin(-150*rad)),0),shaftwidth=0.5,headwidth=0.2,color=color.black)
                    rightedge[j]=arrow(pos=vertex[j].pos,axis=vector((l*cos(-30*rad)),(l*sin(-30*rad)),0),shaftwidth=0.5,headwidth=0.2,color=color.black)
                    temp.append(leftedge[j])
                    temp.append(rightedge[j])
                    child.append(j)
                    child.append(j)
                    j+=1
                else:
                   vertex[j]=sphere(pos=temp[k].axis+temp[k].pos,radius=r,color=color.black)
                   lb[j]=label(pos=vertex[j].pos,text="Null",color=color.white,opacity=0, space=r*4+4, height=r*4+4, box=False)
                   leftedge[j]=arrow(pos=vertex[j].pos,axis=vector((l*cos(-150*rad)),(l*sin(-150*rad)),0),shaftwidth=0.5,headwidth=0.2,color=color.black, visible=False)
                   rightedge[j]=arrow(pos=vertex[j].pos,axis=vector((l*cos(-30*rad)),(l*sin(-30*rad)),0),shaftwidth=0.5,headwidth=0.2,color=color.black, visible=False)
                   if(child[0] not in grp):
                        grp[child[0]]=[-1]
                   else:
                        grp[child[0]].append(-1)
                   j+=1
                temp.pop(0)
                child.pop(0)
        num+=1
        r=r-r/2.2
        l=l-l/2.2
    if(search==1):
        t=0
        fnd.visible=True
        unfnd.visible=True
        l1.visible=True
        l2.visible=True
        if(val[t]==res):
            vertex[t].color=color.blue
            fnd.color=color.green
            return
        pre=vertex[t].color
        vertex[t].color=color.yellow
        while(t in val):
            rate(1)
            if(res<val[t]):
                vertex[t].color=pre
                t=grp[t][0]
                if(t==-1):
                    break
                pre=vertex[t].color
                vertex[t].color=color.yellow
            elif(res>val[t]):
                vertex[t].color=pre
                t=grp[t][1]
                if(t==-1):
                    break
                pre=vertex[t].color
                vertex[t].color=color.yellow
            else:
                vertex[t].color=color.blue
                fnd.color=color.green
                return
                break
        unfnd.color=color.red

bst = RedBlackTree()

def insert_node_(insn):
    print("Enter the number to be inserted")
    num=int(input())
    bst.insert(num)
    bst.pretty_print()
    tree=bst.printLevelOrder()
    visual(tree,0,-1)

insn=button(bind=insert_node_,text='Insert',background=vector(0.88,0.66,0),color=color.white)

#vector(0.22,0.24,0.27) blackish
#vector(1,0.82,0.29) yellowish gold

def search_node_(sern):
    print("Enter the number to be searched")
    num=int(input())
    node=bst.searchTree(num)
    tree=bst.printLevelOrder()
    visual(tree,1,num)
    if(node.data==0):
        print("not found")
    else:
        print("found")

sern=button(bind=search_node_,text='Search',background=vector(0,0.46,0.50),color=color.white)

#vector(0,0.68,0.71) greenish
#vector(0,0.46,0.50) dark greenish

def delete_node_(deln):
    print("Enter the number to be deleted")
    num=int(input())
    bst.remove_node(num)
    bst.pretty_print()
    tree=bst.printLevelOrder()
    visual(tree,0,-1)

deln=button(bind=delete_node_,text='Delete',background=vector(0.16,0.16,0.27),color=color.white)
