## このシステムについて (About the system)
Newfocus8742のピコモータドライバーをEPICSで動かすためのシステムをつくった。(I [Miyo] made a system to run the New Focus 8742 pico driver over EPICS.)

## Pythonスクリプト (Python Scripts)
 * 実際に動かしているファイル (running scripts)： /opt/rtcds/userapps/release/cds/common/scripts/epics-motor-control/picomotor/
  * ./happy_pico_start.py : ユーザーがピコモータを動かすためのスクリプト。(For the user to start the picos.) /kagra/bin/happy_pico_startにシンボリックリンクを貼っているので、コマンドとして利用可能。(There is a symbolic link to this in /kagra/bin, so it can be invoked as happy_pico_start.)
  * ./picomotor/_main_.py : メインファイル。システムを動かすときはこのファイルを呼び出す。(Main file.)
  * ./picomotor/_init_.py : 初期設定ファイル。(Settings file.)
  * ./picomotor/newfocus8742.py : Newfocus８７４２をうごかすためのファイル。(Newfocus 8742 driver.)
  * ./picomotor/pcaspico.py : PCASサーバーをつくるためのファイル。(Creates a PCAS server.)
 * 開発用のファイル： /opt/rtcds/userapps/release/cds/common/scripts/picomotor_test/ (scripts under construction)
  * ファイル構成は上と基本的に同じ。(File structure is fundamentally the same as above.)
  * テストのためのMEDM画面もここにある。(There is also a test MEDM screen.)

## MEDMファイル (MEDM files)
 * 実際に動かしているファイル：/opt/rtcds/userapps/release/cds/common/medm/picomotor/ (Active screens are here.)
  * ./HAPPY_PICO_MASTER.adl : ドライバーの一覧。(Driver overview.)
  * ./HAPPY_PICO_CUST.adl : ドライバーを動かすための画面。(Driver startup.)
