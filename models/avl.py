from models.obstaculo import Obstaculo

class NodoAVL:
    def __init__(self, obstaculo: Obstaculo):
        self.obstaculo = obstaculo
        self.altura = 1
        self.izq = None
        self.der = None

class AVLTree:
    def __init__(self):
        self.raiz = None

    # util
    def _h(self, n): return n.altura if n else 0
    def _bal(self, n): return self._h(n.izq) - self._h(n.der) if n else 0
    def _up(self, n): n.altura = 1 + max(self._h(n.izq), self._h(n.der))

    def _cmp(self, a: Obstaculo, b: Obstaculo):
        # Orden por (x, y)
        if a.x != b.x: return -1 if a.x < b.x else 1
        if a.y != b.y: return -1 if a.y < b.y else 1
        return 0

    # rotaciones
    def _rot_right(self, y):
        x = y.izq; T2 = x.der
        x.der = y; y.izq = T2
        self._up(y); self._up(x)
        return x

    def _rot_left(self, x):
        y = x.der; T2 = y.izq
        y.izq = x; x.der = T2
        self._up(x); self._up(y)
        return y

    # insertar
    def insertar(self, obstaculo: Obstaculo):
        self.raiz = self._insert(self.raiz, obstaculo)

    def _insert(self, nodo, obstaculo):
        if not nodo:
            return NodoAVL(obstaculo)

        c = self._cmp(obstaculo, nodo.obstaculo)
        if c == 0:
            raise ValueError(f"Duplicado en ({obstaculo.x},{obstaculo.y})")
        elif c < 0:
            nodo.izq = self._insert(nodo.izq, obstaculo)
        else:
            nodo.der = self._insert(nodo.der, obstaculo)

        self._up(nodo)
        return self._rebalance(nodo, obstaculo)

    # eliminar
    def eliminar(self, obstaculo: Obstaculo):
        self.raiz = self._delete(self.raiz, obstaculo)

    def _delete(self, nodo, obstaculo):
        if not nodo:
            return None

        c = self._cmp(obstaculo, nodo.obstaculo)
        if c < 0:
            nodo.izq = self._delete(nodo.izq, obstaculo)
        elif c > 0:
            nodo.der = self._delete(nodo.der, obstaculo)
        else:
            # Caso 1: sin hijos
            if not nodo.izq and not nodo.der:
                return None
            # Caso 2: un hijo
            elif not nodo.izq:
                return nodo.der
            elif not nodo.der:
                return nodo.izq
            # Caso 3: dos hijos se busca el menor de la derecha
            else:
                sucesor = self._min_value(nodo.der)
                nodo.obstaculo = sucesor.obstaculo
                nodo.der = self._delete(nodo.der, sucesor.obstaculo)

        self._up(nodo)
        return self._rebalance(nodo, obstaculo)

    def _min_value(self, nodo):
        actual = nodo
        while actual.izq:
            actual = actual.izq
        return actual

    # rebalanceo
    def _rebalance(self, nodo, obstaculo):
        b = self._bal(nodo)

        if b > 1 and self._cmp(obstaculo, nodo.izq.obstaculo) < 0:
            return self._rot_right(nodo)
        if b < -1 and self._cmp(obstaculo, nodo.der.obstaculo) > 0:
            return self._rot_left(nodo)
        if b > 1 and self._cmp(obstaculo, nodo.izq.obstaculo) > 0:
            nodo.izq = self._rot_left(nodo.izq)
            return self._rot_right(nodo)
        if b < -1 and self._cmp(obstaculo, nodo.der.obstaculo) < 0:
            nodo.der = self._rot_right(nodo.der)
            return self._rot_left(nodo)

        return nodo

    # recorridos
    def in_order(self):
        res = []
        self._in(self.raiz, res)
        return res

    def _in(self, n, res):
        if not n: return
        self._in(n.izq, res)
        res.append(n.obstaculo)
        self._in(n.der, res)
