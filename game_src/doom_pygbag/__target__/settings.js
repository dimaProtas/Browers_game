// Transcrypt'ed from Python, 2023-09-07 19:04:05
var math = {};
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as __module_math__ from './math.js';
__nest__ (math, '', __module_math__);
var __name__ = 'settings';
var __left0__ = tuple ([1600, 900]);
export var RES = __left0__;
export var WIDTH = __left0__ [0];
export var HEIGHT = __left0__ [1];
export var HALF_WIDTH = Math.floor (WIDTH / 2);
export var HALF_HEIGHT = Math.floor (HEIGHT / 2);
export var FPS = 0;
export var PLAYER_POS = tuple ([1.5, 5]);
export var PLAYER_ANGLE = 0;
export var PLAYER_SPEED = 0.004;
export var PLAYER_ROT_SPEED = 0.002;
export var PLAYER_SIZE_SCALE = 60;
export var PLAYER_MAX_HEALTH = 100;
export var MOUSE_SENSITIVITY = 0.0003;
export var MOUSE_MAX_REL = 40;
export var MOUSE_BORDER_LEFT = 100;
export var MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT;
export var FLOOR_COLOR = tuple ([30, 30, 30]);
export var FOV = math.pi / 3;
export var HALF_FOV = FOV / 2;
export var NUM_RAYS = Math.floor (WIDTH / 2);
export var HALF_NUM_RAYS = Math.floor (NUM_RAYS / 2);
export var DELTA_ANGLE = FOV / NUM_RAYS;
export var MAX_DEPTH = 20;
export var SCREEN_DIST = HALF_WIDTH / math.tan (HALF_FOV);
export var SCALE = Math.floor (WIDTH / NUM_RAYS);
export var TEXTURE_SIZE = 256;
export var HALF_TEXTURE_SIZE = Math.floor (TEXTURE_SIZE / 2);

//# sourceMappingURL=settings.map