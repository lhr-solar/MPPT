#include "GlobalMPPTAlgorithm.h"
GlobalMPPTAlgorithm::GlobalMPPTAlgorithm(int _globalAlgoType, int _strideType, int _localAlgoType){
    // model = LocalMPPTAlgorithm(-1, _strideType);
    _globalMPPTType = _globalAlgoType;
    if(_localAlgoType == 4){
        model = FeedbackControl(_strideType);
    }else if(_globalMPPTType == 2){
        model = Golden(_strideType);
    }else if(_globalMPPTType == 3){
        model = IncrementalConductance(_strideType);
    }else if(_localAlgoType == 0){
        model = PandO(_strideType);
    }else if(_globalMPPTType == 5){
        model = Ternary(_strideType);
    }else if(_globalMPPTType == 1){
        model = Bisection(_strideType);
    }else{
        model = LocalMPPTAlgorithm(-1,_strideType);
    }
    vOld = 0.0;
    iOld = 0.0;
    pOld = 0.0;
    
}
 
float GlobalMPPTAlgorithm::getReferenceVoltage(float vArr, float cArr, float vBatt, float cBatt){
   if (vArr == 0){
       vOld = vArr;
       iOld = vArr;
       pOld = cArr * cArr;
       return (vArr + .02);
   } 
    float vRef = model.getReferenceVoltage(vArr, cArr, vBatt, cBatt);
    // int (left,right) = _getBounds();
    float left = getLeftBound();
    float right = getRightBound();
 
    if (vRef < left){
       vRef = left;
    }else if (vRef > right){
        vRef = right;
    }
    return vRef;
}
int GlobalMPPTAlgorithm::getGlobalAlgoType(){
    return _globalMPPTType;
}
int GlobalMPPTAlgorithm::getLocalAlgoType(){
    return model.getLocalAlgorithm();
}

const char* GlobalMPPTAlgorithm::getLocalAlgoString(){
    return model.getLocalAlgoType();
}
const char* GlobalMPPTAlgorithm::getStrideType(){
    return model.getStrideType();
}
float GlobalMPPTAlgorithm::getLeftBound(){
    return 0.0;
}
float getRightBound(){
    return 100.0;
}
// bool GlobalMPPTAlgorithm::checkEnvironmentChanges(float irradiance){
//     if (runningHistory < 10){
//         runningHistory.append(irradiance);
//         return false;
//     }else{
//         average = (sum(runningHistory)/(len(runningHistory)));
//         newAverage = average - (runningHistory[0]/10) + (irradiance / 10);
//         percentChange = abs(irradiance - average)/average;
//         cout << average << " "n<<ewAverage << " "<< percentChange << endl;
//         if (percentChange > 0.1){
//             return true;
//         }else:
//             runningHistory.remove(runningHistory[0]);
//             runningHistory.append(irradiance);
//             return false;
//     }
// }
