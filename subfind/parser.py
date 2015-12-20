import logging
from lxml import etree
from lxml.etree import XPathEvalError


class Parser(object):
    def __init__(self, content):
        parser = etree.HTMLParser()

        self.xpath = etree.fromstring(content, parser)

        self.logger = logging.getLogger(self.__class__.__name__)

    def query(self, query, query_type='list', **kwargs):
        try:
            nodes = self.xpath.xpath(query)
        except XPathEvalError as e:
            self.logger.error('Invalid xpath query: %s' % query)
            raise e
        # print query_type
        if query_type == "innerhtml":
            if len(nodes) > 0:
                ret = ''
                if nodes[0].text:
                    ret += nodes[0].text.encode('utf-8')
                for child_node in nodes[0]:
                    ret += etree.tostring(child_node, encoding="UTF-8")

                if nodes[0].tail:
                    ret += nodes[0].tail.encode('utf-8')

                # ret = self.stringify_children(nodes[0])

                if not ret:
                    # This node is text node
                    return etree.tostring(nodes[0], encoding="UTF-8", method='text')

                return ret

            return None
        elif query_type == 'first':
            if len(nodes) > 0:
                return nodes[0]

            return None
        elif query_type == 'innertext':
            if len(nodes) > 0:
                return etree.tostring(nodes[0], encoding="UTF-8", method='text')

            return None
        elif query_type == 'list':
            return nodes

        raise KeyError('Invalid query_type: %s' % query_type)