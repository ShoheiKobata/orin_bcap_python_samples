# orin_bcap_python_samples

b-cap通信を用いたロボット通信サンプルプログラム。
詳しい説明は [こちら](https://shoheikobata.github.io/bcapSamples.github.io/)


## Description

### フォルダ内の説明

- [orin_bcap_python_samples/SimpleSamples](https://github.com/ShoheiKobata/orin_bcap_python_samples/tree/master/SimpleSamples)
簡単なサンプルプログラムを次に示します。b-cap通信を初めて使用する場合は、これらのプログラムを参照することをお勧めします。 
- [orin_bcap_python_samples/3DMouse_Comntroll](https://github.com/ShoheiKobata/orin_bcap_python_samples/tree/master/3DMouse_Controll)
3Dマウスを使ってロボットを操作するプログラムです。 
- [orin_bcap_python_samples/others](https://github.com/ShoheiKobata/orin_bcap_python_samples/tree/master/others) 
このディレクトリーには、これまでに使用されたテストプログラムと、サポートとして作成されたサンプルプログラムが入っています。それぞれのプログラムの内容はプログラムの冒頭に説明文があります。

### Others内のプログラム

- [orin_bcap_python_samples\others\Multithread_bcap_RC8.py](https://github.com/ShoheiKobata/orin_bcap_python_samples/blob/master/others\Multithread_bcap_RC8.py)
b-capを使用してマルチスレッドで実装されたそれぞれのスレッドから同じロボットコントローラに通信するサンプルです。
- [orin_bcap_python_samples\others\sample_calcurate_position.py](https://github.com/ShoheiKobata/orin_bcap_python_samples/blob/master/others\sample_calcurate_position.py)
ロボットの座標系を計算するサンプルプログラムです。 dev,devH コマンドの使用方法がわかります。
- [orin_bcap_python_samples\others\sample_COBOTTA_AutoCal.py](https://github.com/ShoheiKobata/orin_bcap_python_samples/blob/master/others\sample_COBOTTA_AutoCal.py)
COBOTTAのCALSET動作をb-capから実施するサンプルです。
- [orin_bcap_python_samples\others\sample_COBOTTA_gripper.py](https://github.com/ShoheiKobata/orin_bcap_python_samples/blob/master/others\sample_COBOTTA_gripper.py)
COBOTTA専用グリッパを動作させるサンプルプログラムです。RC8の電動ハンドのコマンドとは異なります。
- [orin_bcap_python_samples\others\sample_convert_pos_data.py](https://github.com/ShoheiKobata/orin_bcap_python_samples/blob/master/others\sample_convert_pos_data.py)
P,T,J型への座標の変換プログラムサンプルです。
P2J, T2J, などの使用方法がわかります。
- [orin_bcap_python_samples\others\sample_display_distance.py](https://github.com/ShoheiKobata/orin_bcap_python_samples/blob/master/others\sample_display_distance.py)
動作中の目標位置までの残りの動作距離を表示するサンプルプログラムです。
- [orin_bcap_python_samples\others\sample_extension_hand.py](https://github.com/ShoheiKobata/orin_bcap_python_samples/blob/master/others\sample_extension_hand.py)
RC8コントローラに接続されている電動ハンドを制御するサンプルプログラムです。
- [orin_bcap_python_samples\others\sample_file_object.py](https://github.com/ShoheiKobata/orin_bcap_python_samples/blob/master/others\sample_file_object.py)
ファイルオブジェクトのサンプルプログラムです。ロボットコントローラ内のPacScriptを取得したり書き換えたりすることができます。
- [orin_bcap_python_samples\others\sample_get_error_info.py](https://github.com/ShoheiKobata/orin_bcap_python_samples/blob/master/others\sample_get_error_info.py)
現在発生しているエラーの詳細情報を取得するサンプルです。
- [orin_bcap_python_samples\others\sample_get_plot_position.py](https://github.com/ShoheiKobata/orin_bcap_python_samples/blob/master/others\sample_get_plot_position.py)
ロボットの現在位置を取得し、グラフに描画するサンプルです。
- [orin_bcap_python_samples\others\sample_GetSrvData.py](https://github.com/ShoheiKobata/orin_bcap_python_samples/blob/master/others\sample_GetSrvData.py)
ロボットの現在位置(P型,J型),トルク指令値、手先速度の値を取得するサンプルです。GetSrvDataコマンドでロボットのサーボに関するデータを取得する方法がわかります。
- [orin_bcap_python_samples\others\Sample_N10-W02_bcap.py](https://github.com/ShoheiKobata/orin_bcap_python_samples/blob/master/others\Sample_N10-W02_bcap.py)
COBOTTAオプションカメラ(N10-W02)の画像をb-cap経由で取得するサンプルプログラムです。
- [orin_bcap_python_samples\others\sample_OutRangeAndMove.py](https://github.com/ShoheiKobata/orin_bcap_python_samples/blob/master/others\sample_OutRangeAndMove.py)
OutRangeコマンドで動作しようとしているポジションが可動範囲内か確認してから動作Move命令を実行するサンプルです。
- [orin_bcap_python_samples\others\sample_pallet_calcpos.py](https://github.com/ShoheiKobata/orin_bcap_python_samples/blob/master/others\sample_pallet_calcpos.py)
PacScriptのPallet.CalcPosをb-capで実行するサンプルです。
- [orin_bcap_python_samples\others\sample_pick_and_place.py](https://github.com/ShoheiKobata/orin_bcap_python_samples/blob/master/others\sample_pick_and_place.py)
ピックアンドプレース動作のサンプルプログラムです。動作範囲やハンドのコマンドはCOBOTTAの物を使用しています。Approach, Depaertなどのコマンドがわかります。


## サンプルアプリケーション

サンプルで作成したアプリケーションを格納しています。それぞれのディレクトリ内にあるReadMeを参照ください。

- IO VIEWER
  - [io_viewer ディレクトリ](https://github.com/ShoheiKobata/orin_bcap_python_samples/tree/master/io_viewer_sample)
  - [io_viewer readme](https://github.com/ShoheiKobata/orin_bcap_python_samples/blob/master/io_viewer_sample/readme.md)

- 3DMuse Controller
  - [3DMuse Controller ディレクトリ](https://github.com/ShoheiKobata/orin_bcap_python_samples/tree/master/3DMouse_Controll)
  - [3DMuse Controller readme](https://github.com/ShoheiKobata/orin_bcap_python_samples/blob/master/3DMouse_Controll/README.md)



## Requirement

python=3.*  

## Reference

- b-cap library:  
  
  <https://github.com/DENSORobot/orin_bcap>  

- RC8 ユーザーズマニュアル
  
  <https://www.fa-manuals.denso-wave.com/jp/usermanuals/000006/>

- RC8 プロバイダマニュアル
  
  <https://www.fa-manuals.denso-wave.com/subfolder/jp/usermanuals/img/001511/RC8_ProvGuide_ja.pdf>

- b-CAP 通信仕様書 RC8 用
  
  <https://www.fa-manuals.denso-wave.com/subfolder/jp/usermanuals/img/001511/b-CAP_Guide_RC8_ja.pdf>

