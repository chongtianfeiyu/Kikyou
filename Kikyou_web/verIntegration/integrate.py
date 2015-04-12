#  _*_ coding:utf-8 _*_

from xml.etree import ElementTree
import paramiko 

class CommentedTreeBuilder ( ElementTree.XMLTreeBuilder ):
    def __init__ ( self, html = 0, target = None ):
        ElementTree.XMLTreeBuilder.__init__( self, html, target )
        self._parser.CommentHandler = self.handle_comment
    
    def handle_comment ( self, data ):
        self._target.start( ElementTree.Comment, {} )
        self._target.data( data )
        self._target.end( ElementTree.Comment )

class ElementTreeCDATA(ElementTree.ElementTree):
    def write(self, file, encoding="us-ascii"):
        assert self._root is not None
        if not hasattr(file, "write"):
            file = open(file, "wb")
        if not encoding:
            encoding = "us-ascii"
        elif encoding != "us-ascii":
            file.write("<?xml version=\"1.0\" encoding=\"%s\"?>\n" % encoding)
        self._write(file, self._root, encoding, {})
    def _write(self, file, node, encoding, namespaces):
#        if node.tag =='item':
#            print "hello"
#            text = node.text.encode(encoding)
#            file.write("<item><![CDATA[%s]]></item>" % node.text)
        if node.tag == '![CDATA[':
            print "nononononononononononon"
#            text = node.text.encode(encoding)
#            file.write("\n<![CDATA[%s]]>\n" % text)
        else:
            if not hasattr(file, "write"):
                file = open(file, "wb")
            ElementTreeCDATA._write2(self, file, node, encoding, namespaces)
    def _write2(self, file, node, encoding, namespaces):
        # write XML to file
        tag = node.tag
        if tag is ElementTree.Comment:
            text = node.text.encode(encoding)
            file.write("<!--%s-->" % text)
        elif tag is ElementTree.ProcessingInstruction:
            text = node.text.encode(encoding)
            file.write("<?%s?>" % text)
        else:
            items = node.items()
            xmlns_items = [] # new namespaces in this scope
            try:
                if isinstance(tag, ElementTree.QName) or tag[:1] == "{":
                    tag, xmlns = ElementTree.fixtag(tag, namespaces)
                    if xmlns: xmlns_items.append(xmlns)
            except TypeError:
                ElementTree._raise_serialization_error(tag)
            file.write("<" + ElementTree._encode(tag, encoding))
            if items or xmlns_items:
                items.sort() # lexical order
                for k, v in items:
                    try:
                        if isinstance(k, ElementTree.QName) or k[:1] == "{":
                            k, xmlns = ElementTree.fixtag(k, namespaces)
                            if xmlns: xmlns_items.append(xmlns)
                    except TypeError:
                        ElementTree._raise_serialization_error(k)
                    try:
                        if isinstance(v, ElementTree.QName):
                            v, xmlns = ElementTree.fixtag(v, namespaces)
                            if xmlns: xmlns_items.append(xmlns)
                    except TypeError:
                        ElementTree._raise_serialization_error(v)
                    file.write(" %s=\"%s\"" % (ElementTree._encode(k, encoding),
                                               ElementTree._escape_attrib(v, encoding)))
                for k, v in xmlns_items:
                    file.write(" %s=\"%s\"" % (ElementTree._encode(k, encoding),
                                               ElementTree._escape_attrib(v, encoding)))
            if node.text or len(node):
                file.write(">")
                if node.text:
                    text = node.text.encode(encoding)
                    file.write(text)
                for n in node:
                    self._write(file, n, encoding, namespaces)
                file.write("</" + ElementTree._encode(tag, encoding) + ">")
            else:
                file.write(" />")
            for k, v in xmlns_items:
                del namespaces[v]
        if node.tail:
            tail = node.tail.encode(encoding)
            file.write(tail)