#!/usr/bin/env python
from os import listdir
from os.path import join
from lxml.etree import parse
from collections import defaultdict
from lucene import initVM
initVM()

from meresco.xml import namespaces

namespaces = namespaces.copyUpdate(dict(oa='http://www.w3.org/ns/oa#'))
xpath = namespaces.xpath
xpathFirst = namespaces.xpathFirst


def open_writer(path):
    from java.io import File
    from org.apache.lucene.analysis.core import WhitespaceAnalyzer
    from org.apache.lucene.analysis.standard import StandardAnalyzer
    from org.apache.lucene.index import IndexWriter, IndexWriterConfig
    from org.apache.lucene.store import FSDirectory
    from org.apache.lucene.util import Version
    directory = FSDirectory.open(File(path))
    analyzer = StandardAnalyzer(Version.LUCENE_43)
    config = IndexWriterConfig(Version.LUCENE_43, analyzer)
    writer = IndexWriter(directory, config)
    return writer

def open_searcher(writer):
    from org.apache.lucene.search import IndexSearcher
    reader = writer.getReader()
    searcher = IndexSearcher(reader)
    return reader, searcher

from org.apache.lucene.document import Document, Field, FieldType, TextField, StringField
from org.apache.lucene.util import BytesRef, BytesRefIterator
from org.apache.lucene.index import Term
vectorFieldType = FieldType(TextField.TYPE_NOT_STORED)
vectorFieldType.setIndexed(True)
vectorFieldType.setTokenized(True)
vectorFieldType.setStoreTermVectors(True)
vectorFieldType.setStoreTermVectorPositions(False)

writer = open_writer('data/index')

def addToIndex(lxmlNode):
    uri = xpathFirst(lxmlNode, '//oa:hasTarget/@rdf:resource')
    print uri
    seen = set()
    doc = Document()
    for fieldName in FIELD_NAMES:
        seen.clear()
        for subpath in [
            '', '/*/rdfs:label', '/*/skos:prefLabel', '/*/skos:altLabel',
            '/*/dcterms:title', '/*/foaf:name']:
            for value in xpath(lxmlNode, '//%(fieldName)s%(subpath)s/text()' % locals()):
                if value in seen:
                    continue
                seen.add(value)
                field = Field(INDEX_FIELDS.get(fieldName, fieldName), value, vectorFieldType)
                doc.add(field)
                doc.add(StringField("uri", uri, Field.Store.YES))
    writer.updateDocument(Term("uri", uri), doc)

def read_data():
    datadir = 'data/summaries'
    for name in listdir(datadir):
        path = join(datadir, name)
        with open(path) as f_:
            lxmlNode = parse(f_)
        addToIndex(lxmlNode)

def read_vectors():
    for doc in xrange(0, reader.numDocs()):
        for fieldName in FIELD_NAMES:
            terms = reader.getTermVector(doc, fieldName)
            if terms:
                termsEnum = terms.iterator(None)
                vectors[fieldName][doc] = \
                    set(term.utf8ToString() for term in BytesRefIterator.cast_(termsEnum))

def read_uris():
    with open("data/uris.csv", "w") as f:
        for doc in xrange(0, reader.numDocs()):
            print >> f, "%s;%s" % (doc, reader.document(doc).get("uri"))

vectors = defaultdict(dict)
matrix = defaultdict(dict)

def the_distance(a, b):
    d = float(len(a.intersection(b))) / len(a.union(b)) # jaccard
    return d if d > 0.3 else None

def make_matrix():
    for fieldName, termsets in vectors.iteritems():
        for doc in termsets.iterkeys():
            for other in xrange(0, doc):
                v = vectors.get(fieldName)
                if v:
                    termsOther = v.get(other)
                    if termsOther:
                        d = the_distance(termsets[doc], v[other])
                        if d:
                            matrix[fieldName][(doc,other)] = d
            

FIELD_NAMES = ['dcterms:title', 'dcterms:subject', 'dcterms:creator', 'dcterms:contributor', 'dcterms:date', 'dcterms:description', 'dcterms:type']
INDEX_FIELDS = {
    'dcterms:contributor': 'dcterms:creator'
}

read_data()

reader, searcher = open_searcher(writer)

read_vectors()
read_uris()
make_matrix()
#for field, fieldMatrix in matrix.iteritems():
#    print field, fieldMatrix


def aggregateFieldsEqualWeights():
    aggregatedMatrix = {}
    for doc in xrange(0, reader.numDocs()):
        for other in xrange(0, doc):
            total = 0.0
            for fieldName in FIELD_NAMES:
                value = matrix.get(fieldName, {}).get((doc, other))
                if value:
                    total += value
            if total:
                aggregatedMatrix[(doc, other)] = total / 6
    return aggregatedMatrix

aggregatedMatrix = aggregateFieldsEqualWeights()
with open("result.csv", "w") as f:
    for n in xrange(0, reader.numDocs()):
        f.write("%s;" % n)
    f.write("\n")
    for n in xrange(0, reader.numDocs()):
        f.write("%s;" % n)
        for _ in xrange(0, reader.numDocs()):
            value = aggregatedMatrix.get((n, _), 0)
            f.write("%s;" % value)
        f.write("\n")


writer.close()
reader.close()
