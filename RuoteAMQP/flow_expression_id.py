import re

class FeiException(Exception):
    pass

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

class FlowExpressionId(object):
    """
    The FlowExpressionId (fei for short) is an process expression identifier.
    Each expression when instantiated gets a unique fei.
    
    Feis are also used in workitems, where the fei is the fei of the
    [participant] expression that emitted the workitem.
    
    Feis can thus indicate the position of a workitem in a process tree.
    """

    def __init__(self, wfid, sub_wfid, expid, engine_id = None): 
        """
        @type wfid: string
        @param wfid: workflow instance id, 
                     the identifier for the process instance

        @type sub_wfid: string
        @param sub_wfid: the identifier for the 
                      sub process within the main instance

        @type expid: L{ExpressionId}
        @param expid: the expression id, where in the process tree

        @type engine_id: string
        @param engine_id:  only relevant in multi engine scenarii 
        """
        self._wfid = wfid
        self._sub_wfid = sub_wfid 
        self._expid = expid 
        self._engine_id = engine_id

    @property
    def wfid(self):
        """
        @rtype: C{string}
        @return: The wfid
        """
        return self._wfid

    @property
    def sub_wfid(self):
        """
        @rtype: C{string}
        @return: The sub_wfid
        """
        return self._sub_wfid

    @property 
    def expid(self):
        """
        @rtype: C{string}
        @return: The sub_wfid in form '^\d{0,2}%s\d{0,2}%s\d{0,2}$'
        """
        return str(self._expid)

    @property
    def engine_id(self):
        """
        @rtype: C{string}
        @return: The engine_id
        """
        return self._engine_id

    @property 
    def storage_id(self):
        """
        @rtype: C(string)
        @return: The storage id
        """
        return "%s!%s!%s" % (self.expid, 
                             self.sub_wfid, 
                             self.wfid)

    @property
    def child_id(self):
        """
        @rtype: C{int}
        @return: The last number in the expid
        """
        return self._expid.child_id

    def is_direct_child(self, fei):
        """
        @rtype: C{bool}
        @return: Is this FEI a child of the fei passed 
        """
        ret_val = False
        if all([(getattr(self, prop) == getattr(fei, prop)) 
                for prop in [ "sub_wfid", "wfid", "engine_id" ]]):
            ret_val =  (self._expid.parent_id == fei._expid)
        return ret_val
