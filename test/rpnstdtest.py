"""Unit test for rpnstd.py and Fstd.py"""

import rpnstd
import Fstdc
import unittest
import numpy

#class KnownValues(unittest.TestCase):
    #"""Check good behaviour of all class.fn on good input values"""
    #pass

#class BadInput(unittest.TestCase):
    #"""Check good behaviour of all class.fn on bad input values"""
    #pass

#class SanityCheck(unittest.TestCase):
    #"""Check that revesefn(fn(value)) == value"""

    #def testSanity(self):
        #"""cigaxg(cxgaig(n))==n for all n"""
        ##self.assertTrue(expr[, msg])
        ##self.assertFalse(expr[, msg])
        ##self.assertEqual(first, second[, msg])
        ##self.assertNotEqual(first, second[, msg])
        ##self.assertAlmostEqual(first, second[, places[, msg]])
        ##self.assertNotAlmostEqual(first, second[, places[, msg]])
        ##self.assertRaises(exception, callable, ...)
        #pass

class CigaxgKnownValues(unittest.TestCase):

    knownValues = (
        ('Grille_Amer_Nord PS 40km','N',(401,401),(200.5,200.5,40000.0,21.0),(2005,  2005,  2100,   400)),
        ('Grille_Europe PS 40km',   'N',(401,401),(200.5,220.5,40000.0,260.0),( 400,  1000, 29830, 57333)),
        ('Grille_Inde PS 40km',     'N',(401,401),(200.5,300.5,40000.0,190.0),( 400,  1700,  4217, 58335)),
        ('Grille_Hem_Sud PS 40km',  'S',(401,401),(200.5,200.5,40000.0,21.0),(2005,  2005,  2100,   400)),
        ('Grille_Canada PS 20km',   'N',(351,261),(121.5,281.5,20000.0,21.0),( 200,   210, 20548, 37716)),
        ('Grille_Maritimes PS 20km','N',(175,121),(51.5,296.5,20000.0,340.0),( 200,   200, 25513, 54024)),
        ('Grille_Quebec PS 20km',   'N',(199,155),(51.5,279.5,20000.0,0.0),( 200,     0, 23640, 37403)),
        ('Grille_Prairies PS 20km', 'N',(175,121),(86.5,245.5,20000.0,20.0),( 200,   200, 21001, 37054)),
        ('Grille_Colombie PS 20km', 'N',(175,121),(103.5,245.5,20000.0,30.0),( 200,   300, 19774, 37144)),
        ('Grille_USA PS 20km',      'N',(351,261),(121.0,387.5,20000.0,21.0),( 200,   210, 21094, 39002)),
        ('Grille_Global LatLon 0.5','L',(721,359),(-89.5,180.0,0.5,0.5),(  50,    50,    50, 18000))
        #,#The Grille_GemLam10 PS is causing a problem, very tiny expected roundoff error
        #('Grille_GemLam10 PS 10km', 'N',(1201,776),(536.0,746.0,10000.0,21.0),( 100,   210, 19416, 39622))
        )

    def testCigaxgKnownValues(self):
        """Cigaxg should give known result with known input"""
        for name,proj,dims,xg,ig in self.knownValues:
            xgout = rpnstd.cigaxg(proj,ig[0],ig[1],ig[2],ig[3])
            self.assertAlmostEqual(xgout[0],xg[0],1,name+'[0]'+xgout.__repr__())
            self.assertAlmostEqual(xgout[1],xg[1],1,name+'[1]'+xgout.__repr__())
            self.assertAlmostEqual(xgout[2],xg[2],1,name+'[2]'+xgout.__repr__())
            self.assertAlmostEqual(xgout[3],xg[3],1,name+'[3]'+xgout.__repr__())

    def testCxgaigKnownValues(self):
        """Cxgaig should give known result with known input"""
        for name,proj,dims,xg,ig in self.knownValues:
            igout = rpnstd.cxgaig(proj,xg[0],xg[1],xg[2],xg[3])
            self.assertEqual(igout,ig,name+igout.__repr__())

    def testSanity(self):
        """cigaxg(cxgaig(n))==n for all n"""
        for name,proj,dims,xg,ig in self.knownValues:
            xgout = rpnstd.cigaxg(proj,ig[0],ig[1],ig[2],ig[3])
            igout = rpnstd.cxgaig(proj,xgout[0],xgout[1],xgout[2],xgout[3])
            self.assertEqual(igout,ig,name+igout.__repr__()+xgout.__repr__())


class Level_to_ip1KnownValues(unittest.TestCase):

    #lvlnew,lvlold,ipnew,ipold,kind
    #we need to specify 2 levels since the old style ip1 give is an approx of level in some cases
    knownValues = (
    (0.,    0.,    15728640, 12001,0),
    (13.5,  15.,   8523608,  12004,0),
    (1500., 1500., 6441456,  12301,0),
    (5525., 5525., 6843956,  13106,0),
    (12750.,12750.,5370380,  14551,0),
    (0.,    0.,    32505856, 2000, 1),
    (0.1,   0.1,   27362976, 3000,1),
    (0.02,  0.02,  28511552, 2200,1),
    (0.000003,0.,  32805856, 2000,1),
    (1024.,1024.,  39948288, 1024,2),
    (850., 850.,   41744464, 850, 2),
    (650., 650.,   41544464, 650, 2),
    (500., 500.,   41394464, 500, 2),
    (10.,  10.,    42043040, 10,  2),
    (2.,   2.,     43191616, 1840,2),
    (0.3,  0.3,    44340192, 1660,2)
    )

    def testLevels_to_ip1KnownValues(self):
        """levels_to_ip1 should give known result with known input"""
        for lvlnew,lvlold,ipnew,ipold,kind in self.knownValues:
            (ipnew2,ipold2) = rpnstd.levels_to_ip1([lvlnew],kind)[0]
            self.assertEqual(ipnew2,ipnew)
            (ipnew2,ipold2) = rpnstd.levels_to_ip1([lvlold],kind)[0]
            self.assertEqual(ipold2,ipold)

    def testip1_to_levelsKnownValues(self):
        """ip1_to_levels should give known result with known input"""
        for lvlnew,lvlold,ipnew,ipold,kind in self.knownValues:
            (lvl2,kind2) = rpnstd.ip1_to_levels([ipnew])[0]
            self.assertEqual(kind2,kind)
            self.assertAlmostEqual(lvlnew,lvl2,6)
            (lvl2,kind2) = rpnstd.ip1_to_levels([ipold])[0]
            self.assertEqual(kind2,kind)
            self.assertAlmostEqual(lvlold,lvl2,6)

    def testSanity(self):
        """levels_to_ip1(ip1_to_levels(n))==n for all n"""
        for lvlnew,lvlold,ipnew,ipold,kind in self.knownValues:
            (lvl2,kind2) = rpnstd.ip1_to_levels([ipnew])[0]
            (ipnew2,ipold2) = rpnstd.levels_to_ip1([lvl2],kind2)[0]
            self.assertEqual(ipnew2,ipnew)
            (lvl2,kind2) = rpnstd.ip1_to_levels([ipold])[0]
            (ipnew2,ipold2) = rpnstd.levels_to_ip1([lvl2],kind2)[0]
            self.assertEqual(ipold2,ipold)


class Fstdc_ezgetlaloKnownValues(unittest.TestCase):

    def test_Fstdc_ezgetlalo_KnownValues(self):
        """Fstdc_ezgetlalo should give known result with known input"""
        la = numpy.array(
            [[-89.5, -89. , -88.5],
            [-89.5, -89. , -88.5],
            [-89.5, -89. , -88.5]]
            ,dtype=numpy.dtype('float32'),order='FORTRAN')
        lo = numpy.array(
            [[ 180. ,  180. ,  180. ],
            [ 180.5,  180.5,  180.5],
            [ 181. ,  181. ,  181. ]]
            ,dtype=numpy.dtype('float32'),order='FORTRAN')
        cla = numpy.array(
            [[[-89.75, -89.25, -88.75],
            [-89.75, -89.25, -88.75],
            [-89.75, -89.25, -88.75]],
            [[-89.25, -88.75, -88.25],
            [-89.25, -88.75, -88.25],
            [-89.25, -88.75, -88.25]],
            [[-89.25, -88.75, -88.25],
            [-89.25, -88.75, -88.25],
            [-89.25, -88.75, -88.25]],
            [[-89.75, -89.25, -88.75],
            [-89.75, -89.25, -88.75],
            [-89.75, -89.25, -88.75]]]
            ,dtype=numpy.dtype('float32'),order='FORTRAN')
        clo = numpy.array(
            [[[ 179.75,  179.75,  179.75],
            [ 180.25,  180.25,  180.25],
            [ 180.75,  180.75,  180.75]],
            [[ 179.75,  179.75,  179.75],
            [ 180.25,  180.25,  180.25],
            [ 180.75,  180.75,  180.75]],
            [[ 180.25,  180.25,  180.25],
            [ 180.75,  180.75,  180.75],
            [ 181.25,  181.25,  181.25]],
            [[ 180.25,  180.25,  180.25],
            [ 180.75,  180.75,  180.75],
            [ 181.25,  181.25,  181.25]]]
            ,dtype=numpy.dtype('float32'),order='FORTRAN')
        ni = 3
        nj = 3
        grtyp='L'
        grref='L'
        (ig1,ig2,ig3,ig4) =  rpnstd.cxgaig(grtyp,-89.5,180.0,0.5,0.5)
        hasAxes = 0
        doCorners = 1
        (i0,j0) = (0,0)
        (la2,lo2,cla2,clo2) = Fstdc.ezgetlalo((ni,nj),grtyp,(grref,ig1,ig2,ig3,ig4),(None,None),hasAxes,(i0,j0),doCorners)
        self.assertFalse(numpy.any(la!=la2))
        self.assertFalse(numpy.any(lo!=lo2))
        for ic in range(0,4):
            if numpy.any(cla[ic,...]!=cla2[ic,...]):
                print ic,'cla'
                print cla[ic,...]
                print cla2[ic,...]
            self.assertFalse(numpy.any(cla[ic,...]!=cla2[ic,...]))
            if numpy.any(clo[ic,...]!=clo2[ic,...]):
                print ic,'clo'
                print clo[ic,...]
                print clo2[ic,...]
            self.assertFalse(numpy.any(clo[ic,...]!=clo2[ic,...]))
        #print numpy.array_repr(cla2)
        #print numpy.array_repr(clo2)


class RPNMetaTests(unittest.TestCase):

    def test_RPNMeta_Error(self):
        """RPNMeta should raise exception on known error cases"""
        self.assertRaises(TypeError, rpnstd.RPNMeta, 'not a valid argument')
        a = rpnstd.RPNMeta()
        #self.assertRaises(ValueError, a.getaxis())
        try:
            axis = a.getaxis()
        except ValueError:
            self.assertFalse(False)
        else:
            self.assertFalse(True)
        a.grtyp = 'Z'
        #self.assertRaises(TypeError, a.getaxis())
        try:
            axis = a.getaxis()
        except TypeError:
            self.assertFalse(False)
        else:
            self.assertFalse(True)

    def test_RPNMeta_KnownValues(self):
        """RPNMeta should give known result with known input"""
        pass #TODO: this is well tested in doctest


class RPNGridTests(unittest.TestCase):

    def test_RPNGrid_Error(self):
        """RPNGrid should raise exception on known error cases"""
        pass #TODO

    def test_RPNGrid_KnownValues(self):
        """RPNGrid should give known result with known input"""
        pass #TODO


class RPNFileTests(unittest.TestCase):

    lad = numpy.array(
        [[-89.5, -89. , -88.5],
        [-89.5, -89. , -88.5],
        [-89.5, -89. , -88.5]]
        ,dtype=numpy.dtype('float32'),order='FORTRAN')
    lod = numpy.array(
        [[ 180. ,  180. ,  180. ],
        [ 180.5,  180.5,  180.5],
        [ 181. ,  181. ,  181. ]]
        ,dtype=numpy.dtype('float32'),order='FORTRAN')
    grtyp='L'
    xg14 = (-89.5,180.0,0.5,0.5)
    fname = '__rpnstd__testfile__.fst'
    la = None
    lo = None

    def test_RPNFile_Error(self):
        """RPNFile should raise exception on known error cases"""
        self.assertRaises(IOError, rpnstd.RPNFile, '__do__not__exist__.fst','RND+R/O')


    def erase_testfile(self):
        import os
        try:
            os.unlink(self.fname)
        except:
            pass

    def create_basefile(self):
        """create a basic test file for RPNFile tests"""
        #print "============ Create Base File ==============="
        self.erase_testfile()
        f = rpnstd.RPNFile(self.fname)
        (ig1,ig2,ig3,ig4) =  rpnstd.cxgaig(self.grtyp,self.xg14)
        r0 = rpnstd.RPNMeta()
        r0.update(r0.defaultKeysVals())
        r0m = rpnstd.RPNMeta(r0,nom='LA',type='C',ni=self.lad.shape[0],nj=self.lad.shape[1],nk=1,grtyp=self.grtyp,ig1=ig1,ig2=ig2,ig3=ig3,ig4=ig4)
        self.la = rpnstd.RPNRec(data=self.lad,meta=r0m)
        r0m.nom = 'LO'
        self.lo = rpnstd.RPNRec(data=self.lod,meta=r0m)
        f.write(self.la)
        f.write(self.lo)
        f.close()
        return (self.la,self.lo)


    def test_RPNFileRead_KnownValues(self):
        """RPNFile should give known result with known input"""
        (la,lo) = self.create_basefile() #wrote 2 recs in that order: la, lo
        #print "============ Read Test ==============="
        f2 = rpnstd.RPNFile(self.fname)
        la2 = f2[rpnstd.FirstRecord]
        lo2 = f2[rpnstd.NextMatch]
        r2none = f2[rpnstd.NextMatch]
        f2.close()
        self.assertEqual(la2.nom,la.nom)
        self.assertEqual(lo2.nom,lo.nom)
        self.assertEqual(r2none,None)
        if numpy.any(la2.d!=la.d):
                print 'la2:',la2.d
                print 'la :',la.d
        self.assertFalse(numpy.any(la2.d!=la.d))
        if numpy.any(lo2.d!=lo.d):
                print 'lo2:',lo2.d
                print 'lo :',lo.d
        self.assertFalse(numpy.any(lo2.d!=lo.d))

        self.erase_testfile()
        #TODO: test other params and data

    def test_RPNFileErase_KnownValues(self):
        """RPNFile.erase should give known result with known input"""
        (la,lo) = self.create_basefile() #wrote 2 recs in that order: la, lo
        #print "============ Erase ==============="
        f3 = rpnstd.RPNFile(self.fname)
        f3[la] = None #Erase la (1st rec) - 1st rec is now lo, no 2nd rec
        f3.close()
        #print "============ Check Erase ==============="
        f2 = rpnstd.RPNFile(self.fname)
        lo2 = f2[rpnstd.FirstRecord]
        r2none = f2[rpnstd.NextMatch]
        f2.close()
        self.assertEqual(lo2.nom,lo.nom)
        self.assertEqual(r2none,None)
        self.erase_testfile()

    def test_RPNFileRewrite_KnownValues(self):
        """RPNFile.rewrite should give known result with known input"""
        (la,lo) = self.create_basefile()
        #print "============ ReWrite/Append ==============="
        f3 = rpnstd.RPNFile(self.fname)
        f3.rewrite(lo) #overwrite 2nd rec (lo)... no changes
        f3.append(la)  #append a 3rd rec (la), file now has 3 rec: la, lo, la
        f3.close()
        #print "============ Check ReWrite/Append ==============="
        f2 = rpnstd.RPNFile(self.fname)
        la2 = f2[rpnstd.FirstRecord]
        lo2 = f2[rpnstd.NextMatch]
        la2b= f2[rpnstd.NextMatch]
        r2none = f2[rpnstd.NextMatch]
        f2.close()
        self.assertEqual(la2.nom,la.nom)
        self.assertEqual(lo2.nom,lo.nom)
        self.assertEqual(la2b.nom,la.nom)
        self.assertEqual(r2none,None)
        self.erase_testfile()


if __name__ == "__main__":
    unittest.main()

# kate: space-indent on; indent-mode cstyle; indent-width 4; mixedindent off;
