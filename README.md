1. Crie o diretório de imagens e baixe os dados de calibração (ou insira suas próprias imagens na pasta `imagens/` se for realizar a calibração com suas câmeras):
   ```bash
   python3 download_samples.py
   ```
2. Execute a calibração (isso salvará `parametros_camera.npz` e a imagem sem distorção):
   ```bash
   python3 calibrar_camera.py
   ```
3. Execute o experimento de mapeamento 3D:
   ```bash
   python3 experimento_projecao.py
   ```
4. Se desejar, execute o script extra de calibração estéreo:
   ```bash
   python3 calibracao_estereo.py
   ```
