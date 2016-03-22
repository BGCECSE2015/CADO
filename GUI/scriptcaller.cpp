#include "scriptcaller.h"

ScriptCaller::ScriptCaller(){

}

void ScriptCaller::callScript(std::string parameter){
    system(parameter.c_str());
}
