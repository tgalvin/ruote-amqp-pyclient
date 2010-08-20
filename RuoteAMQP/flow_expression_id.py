import re

ENGINE = 'engine'
CHILD_SEP = "_"
EXPID_PATTERN = "^\d{0,2}%s\d{0,2}%s\d{0,2}$"%(CHILD_SEP, CHILD_SEP)

class FeiException(Exception):
    pass

class FlowExpressionId(object):
    """
    The FlowExpressionId (fei for short) is an process expression identifier.
    Each expression when instantiated gets a unique fei.
    
    Feis are also used in workitems, where the fei is the fei of the
    [participant] expression that emitted the workitem.
    
    Feis can thus indicate the position of a workitem in a process tree.
    """

    def __init__(self, wfid, sub_wfid, expid, engine_id = ENGINE): 
        """
        @type wfid: string
        @param wfid: workflow instance id, 
                     the identifier for the process instance

        @type sub_wfid: string
        @param sub_wfid: the identifier for the 
                      sub process within the main instance

        @type expid: string
        @param expid: the expression id, where in the process tree

        @type engine_id: string
        @param engine_id:  only relevant in multi engine scenarii 
        """
        self.wfid = wfid
        self.sub_wfid = sub_wfid 

        if re.match(EXPID_PATTERN, expid) is None:
            raise FeiException("Unexpected expid: '%s'"% (expid))
        self.expid = expid 
        self.engine_id = engine_id

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

        @rtype: C(int)
        @return: The last number in the expid
        """
        return int(self.expid.split(CHILD_SEP)[-1])
      
