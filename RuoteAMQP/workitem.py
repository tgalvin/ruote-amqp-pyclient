import simplejson as json

class Parameters(object):
    
    forget = None

class Fields(object):

    __result__ = False
    __timed_out__ = False
    __error__ = None

    def __init__(self, result, timed_out, error, dispatched_at, forget):
        self.__result__ = result
        self.__timed_out__ = timed_out
        self.__error__ = error
        self.dispatched_at = dispatched_at
        self.parameters = Parameters()
        self.parameters.forget = forget

from flow_expression_id import FlowExpressionId

def fei_factory(fei_dict):
    fei = FlowExpressionId(fei_dict['wfid'],
                           fei_dict['sub_wfid'],
                           fei_dict['expid'],
                           fei_dict.get('engine_id', None))
    return fei


def fields_factory(fields_dict):
    result = fields_dict['__result__']
    timed_out = fields_dict['__timed_out__']
    error = fields_dict['__error__']
    dispatched_at = fields_dict['dispatched_at']
    forget = fields_dict['params']['forget']
    fields = Fields(result, timed_out, error, dispatched_at, forget)
    return fields


class Workitem(object):

    def __init__(self, message):
        message_dict = json.loads(message)
        self._message_dict = message_dict 
        self.fei = fei_factory(message_dict['fei'])
        self.fields = fields_factory(message_dict['fields'])
        self.participant_name = message_dict['participant_name']

    #################################
    # Delegates 
    #################################

    # FIXME do we really want to retain these?

    @property
    def sid(self):
        """
        @type sid: C{string}
        @param sid: The storage id
        """
        return self.fei.storage_id

    @property 
    def wfid(self):
        """
        @type wfid: C{string}
        @param wfid: The workflow id
        """
        return self.fei.wfid

    @property 
    def result(self):
        """
        @type result: C{bool}
        @param result: The result
        """
        return self.fields.__result__

    @property 
    def dispatch_at(self):
        """
        @type dispatch_at: C{string}
        @param dispatch_at: The dispatch location
        """
        
        return self.fields.dispatched_at

    @property 
    def forget(self):
        """
        @type forget: C{string}
        @param forget: FIXME
        """
        return self.fields.parameters.forget

    @property 
    def timed_out(self):
        """
        @type timed_out: C{bool}
        @param timed_out: Has it timed out
        """
        return self.fields.__timed_out__

    @property 
    def error(self):
        """
        @type error: C{string}
        @param error: The workflow id
        """
        return self.fields.__error__

    @property 
    def parameters(self):
        """
        @type parameters: L{Parameters]
        @param parameters: The Ruote Parameters
        """
        
        return self.fields.parameters
