class ExpressionId(object):
    """
    The ExpressionId
    FIXME more documentation
    """

    CHILD_SEP = "_"

    def __init__(self, *args):
        self.args = args

    def __iter__(self):
        """
        @ytype: C{int}
        @yield: The arguments that make up the ExpressionId 
        """
        for arg in self.args: yield int(arg)

    def __str__(self):
        """
        @rtype: C{string}
        @return:form '^\d{0,2}%s\d{0,2}%s\d{0,2}$'
        """
        return self.CHILD_SEP.join([str(arg) for arg in self])

    @property 
    def child_id(self):
        """
        @rtype: C{int}
        @return: The child id
        """
        return int(self.args[-1]) 

    @property 
    def parent_id(self):
        """
        @rtype: L{ExpressionId}
        @return: The ExpressionId of the parent
        """
        return ExpressionId(*self.args[:-1])

    def __eq__(self, expression_id):
        """
        @rtype: C{bool}
        @return: Are the ExpressionIds equal
        """
        return (self.args == expression_id.args)
