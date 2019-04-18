package ${package_name}

import (
    "encoding/json"
    "errors"
)

type ErrCode int

const (
% for err_info in err_infos:
   ${err_info.code} ErrCode = ${err_info.number}
% endfor
)

var ErrMsgMap = map[ErrCode]string {
% for err_info in err_infos:
    ${err_info.code}:"${err_info.msg}",
% endfor
}

type CustomError struct {
    RetCode ErrCode  `json:"retCode"`
    Message string   `json:"message"`
}

func (ce *CustomError)ToError()(error) {
    bError, _ := json.Marshal(ce)
    return errors.New(string(bError))
}

func genError(errCode ErrCode) (err error) {
    bError, _ := json.Marshal(CustomError{errCode, ErrMsgMap[errCode]})
    return errors.New(string(bError))
}
