import math
import re
from sympy.plotting import plot_implicit
from sympy.parsing.sympy_parser import parse_expr
import quantities as q
from quantulum3 import parser
from simpleeval import simple_eval, NumberTooHigh, InvalidExpression
from utils.cache import gen_cache_name
from utils.mathutils import get_units

async def convert(fro, to):
    try:
        fro = get_units(parser.parse(fro)[0].surface)
        fro[1] = fro[1].strip()
        #lazy check for temps lol
        if to.strip().lower() in ["f", "c", "k"]:
            to = f"deg{to}"
        if fro[1].lower() in ["f", "c", "k"]:
            fro[1] = f"deg{fro[1]}"
        quant = q.Quantity(float(fro[0]), fro[1])
        quant.units = to
        ret = f"{' '.join(fro)} -> {quant}"
    except IndexError:
        return ("Something went wrong! Check spelling and only use the actual word or official short form when writing units.", False)
    except ValueError:
        return (f"Something went wrong! Cannot convert between the units `{fro[1]}` and `{to}`!", False)
    except LookupError:
        return (f"One of `{fro[1]}` or `{to}` are spelled incorrectly or do not exist! \n **NOTE**: Do not make short forms plural (ex, use \"sec\" rather than \"secs\" ;) )!", False)
    except Exception:
        return ("Something went wrong!", False)
    return (ret, True)

functions = {"log": lambda x: math.log(x),
                 "ln": lambda x: math.log(x, math.e),
                 "sin": lambda x: math.sin(x),
                 "cos": lambda x: math.cos(x),
                 "tan": lambda x: math.tan(x),
                 "arcsin": lambda x: math.asin(x),
                 "arccos": lambda x: math.acos(x),
                 "arctan": lambda x: math.atan(x),
                 "sqrt": lambda x: math.sqrt(x)
                 }

async def evaluate(expression):
    ret = "Evaluated expression:"
    clean_expression = expression.replace("^", "**").replace("pi", str(math.pi)).replace("e", str(math.e)).replace(" ", "")
    for i in re.findall("[^=]=[^=]", clean_expression):
        clean_expression = clean_expression.replace(i, f"{i[0]}=={i[-1]}")
    try:
        ret += f"```python\n" \
              f"{expression}\n\n" \
              f"=\n\n" \
              f"{simple_eval(clean_expression, functions=functions)}" \
              f"```"
    except NumberTooHigh:
        return ("Something went wrong! That number is too large to evaluate!", False)
    except InvalidExpression:
        return ("Something went wrong! That is an invalid expression!", False)
    except Exception:
        return ("Something went wrong!", False)
    return (ret, True)

def graph(expression):
    l, r = expression.replace("^", "**").split("=")
    l, r = l.strip(), r.strip()
    plot = plot_implicit(parse_expr(l) - parse_expr(r), show=False)
    plot.title = "Generated by STEMbot :)"
    im_id = "test"#gen_cache_name()
    path = f'../caches/graphs/{im_id}.png'
    plot.save(path)
    return path

if __name__ == "__main__":
    print(graph("y = tan(x)"))