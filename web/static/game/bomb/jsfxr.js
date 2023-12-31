/**
 * SfxrParams
 * 
 * Copyright 2010 Thomas Vian
 *
 * Licensed under the Apache License, Version 2.0 (the 'License');
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an 'AS IS' BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * 
 * @author Thomas Vian
 */
function SfxrParams() {
  //--------------------------------------------------------------------------
  //  
  //  Settings String Methods
  //
  //--------------------------------------------------------------------------

  /**
   * Parses a settings string into the parameters
   * @param  string  Settings string to parse
   * @return      If the string successfully parsed
   */
  this.setSettingsString = function setSettingsString(string)
  {
    var values = string.split(',');
    var a = this;
    a.waveType =         parseInt(values[0]) || 0;
    a.attackTime =        parseFloat(values[1]) || 0;
    a.sustainTime =        parseFloat(values[2]) || 0;
    a.sustainPunch =      parseFloat(values[3]) || 0;
    a.decayTime =        parseFloat(values[4]) || 0;
    a.startFrequency =      parseFloat(values[5]) || 0;
    a.minFrequency =      parseFloat(values[6]) || 0;
    a.slide =          parseFloat(values[7]) || 0;
    a.deltaSlide =        parseFloat(values[8]) || 0;
    a.vibratoDepth =      parseFloat(values[9]) || 0;
    a.vibratoSpeed =      parseFloat(values[10]) || 0;
    a.changeAmount =      parseFloat(values[11]) || 0;
    a.changeSpeed =        parseFloat(values[12]) || 0;
    a.squareDuty =        parseFloat(values[13]) || 0;
    a.dutySweep =        parseFloat(values[14]) || 0;
    a.repeatSpeed =        parseFloat(values[15]) || 0;
    a.phaserOffset =      parseFloat(values[16]) || 0;
    a.phaserSweep =        parseFloat(values[17]) || 0;
    a.lpFilterCutoff =      parseFloat(values[18]) || 0;
    a.lpFilterCutoffSweep =    parseFloat(values[19]) || 0;
    a.lpFilterResonance =    parseFloat(values[20]) || 0;
    a.hpFilterCutoff =      parseFloat(values[21]) || 0;
    a.hpFilterCutoffSweep =    parseFloat(values[22]) || 0;
    a.masterVolume =       parseFloat(values[23]) || 0;
  }   
  
}

/**
 * SfxrSynth
 * 
 * Copyright 2010 Thomas Vian
 *
 * Licensed under the Apache License, Version 2.0 (the 'License');
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an 'AS IS' BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * 
 * @author Thomas Vian
 */
function SfxrSynth() {
  // All variables are kept alive through function closures

  //--------------------------------------------------------------------------
  //
  //  Sound Parameters
  //
  //--------------------------------------------------------------------------
  
  this._params = new SfxrParams();  // Params instance

  //--------------------------------------------------------------------------
  //
  //  Synth Variables
  //
  //--------------------------------------------------------------------------
  
  var _masterVolume;          // masterVolume * masterVolume (for quick calculations)
  
  var _waveType;              // The type of wave to generate
  
  var _envelopeVolume;          // Current volume of the envelope
  var _envelopeStage;            // Current stage of the envelope (attack, sustain, decay, end)
  var _envelopeTime;          // Current time through current enelope stage
  var _envelopeLength;          // Length of the current envelope stage
  var _envelopeLength0;        // Length of the attack stage
  var _envelopeLength1;        // Length of the sustain stage
  var _envelopeLength2;        // Length of the decay stage
  var _envelopeOverLength0;      // 1 / _envelopeLength0 (for quick calculations)
  var _envelopeOverLength1;      // 1 / _envelopeLength1 (for quick calculations)
  var _envelopeOverLength2;      // 1 / _envelopeLength2 (for quick calculations)
  
  var _sustainPunch;          // The punch factor (louder at begining of sustain)
  
  var _phase;                // Phase through the wave
  var _period;              // Period of the wave
  var _maxPeriod;            // Maximum period before sound stops (from minFrequency)
  
  var _slide;              // Note slide
  var _deltaSlide;            // Change in slide
  var _minFreqency;          // Minimum frequency before stopping
  
  var _changeAmount;          // Amount to change the note by
  var _changeTime;            // Counter for the note change
  var _changeLimit;            // Once the time reaches this limit, the note changes
  
  var _squareDuty;            // Offset of center switching point in the square wave
  var _dutySweep;            // Amount to change the duty by
  
  var _filters;            // If the filters are active
  var _lpFilterDeltaPos;        // Change in low-pass wave position, as allowed by the cutoff and damping
  var _lpFilterCutoff;          // Cutoff multiplier which adjusts the amount the wave position can move
  var _lpFilterDeltaCutoff;      // Speed of the low-pass cutoff multiplier
  var _lpFilterDamping;        // Damping muliplier which restricts how fast the wave position can move
  var _lpFilterOn;          // If the low pass filter is active
  
  var _hpFilterPos;          // Adjusted wave position after high-pass filter
  var _hpFilterCutoff;          // Cutoff multiplier which adjusts the amount the wave position can move
  var _hpFilterDeltaCutoff;      // Speed of the high-pass cutoff multiplier
  
  var _noiseBuffer;      // Buffer of random values used to generate noise
  
  //--------------------------------------------------------------------------
  //  
  //  Synth Methods
  //
  //--------------------------------------------------------------------------
  
  /**
   * Resets the runing variables from the params
   * Used once at the start (total reset) and for the repeat effect (partial reset)
   * @param  totalReset  If the reset is total
   */
  this.reset = function reset(totalReset) {
    // Shorter reference
    var p = this._params;
    
    _period = 100.0 / (p.startFrequency * p.startFrequency + 0.001);
    _maxPeriod = 100.0 / (p.minFrequency * p.minFrequency + 0.001);
    
    _slide = 1.0 - p.slide * p.slide * p.slide * 0.01;
    _deltaSlide = -p.deltaSlide * p.deltaSlide * p.deltaSlide * 0.000001;
    
    if (p.waveType == 0) {
      _squareDuty = 0.5 - p.squareDuty * 0.5;
      _dutySweep = -p.dutySweep * 0.00005;
    }
    
    if (p.changeAmount > 0.0) {
      _changeAmount = 1.0 - p.changeAmount * p.changeAmount * 0.9;
    } else {
      _changeAmount = 1.0 + p.changeAmount * p.changeAmount * 10.0;
    }
    
    _changeTime = 0;
    
    if(p.changeSpeed == 1.0) {
      _changeLimit = 0;
    } else {
      _changeLimit = (1.0 - p.changeSpeed) * (1.0 - p.changeSpeed) * 20000 + 32;
    }
    
    if(totalReset) {
      p.paramsDirty = false;
      _masterVolume = p.masterVolume * p.masterVolume;
      
      _waveType = p.waveType;
      
      if (p.sustainTime < 0.01) {
        p.sustainTime = 0.01;
      }
      
      var totalTime = p.attackTime + p.sustainTime + p.decayTime;
      if (totalTime < 0.18) {
        var multiplier = 0.18 / totalTime;
        p.attackTime *= multiplier;
        p.sustainTime *= multiplier;
        p.decayTime *= multiplier;
      }
      
      _sustainPunch = p.sustainPunch;
      
      _phase = 0;
      
      _minFreqency = p.minFrequency;
      
      _filters = p.lpFilterCutoff != 1.0 || p.hpFilterCutoff != 0.0;
      
      _lpFilterPos = 0.0;
      _lpFilterDeltaPos = 0.0;
      _lpFilterCutoff = p.lpFilterCutoff * p.lpFilterCutoff * p.lpFilterCutoff * 0.1;
      _lpFilterDeltaCutoff = 1.0 + p.lpFilterCutoffSweep * 0.0001;
      _lpFilterDamping = 5.0 / (1.0 + p.lpFilterResonance * p.lpFilterResonance * 20.0) * (0.01 + _lpFilterCutoff);
      if (_lpFilterDamping > 0.8) {
        _lpFilterDamping = 0.8;
      }
      _lpFilterDamping = 1.0 - _lpFilterDamping;
      _lpFilterOn = p.lpFilterCutoff != 1.0;
      
      _hpFilterPos = 0.0;
      _hpFilterCutoff = p.hpFilterCutoff * p.hpFilterCutoff * 0.1;
      _hpFilterDeltaCutoff = 1.0 + p.hpFilterCutoffSweep * 0.0003;
      
      _envelopeVolume = 0.0;
      _envelopeStage = 0;
      _envelopeTime = 0;
      _envelopeLength0 = p.attackTime * p.attackTime * 100000.0;
      _envelopeLength1 = p.sustainTime * p.sustainTime * 100000.0;
      _envelopeLength2 = p.decayTime * p.decayTime * 100000.0 + 10;
      _envelopeLength = _envelopeLength0;
      this._envelopeFullLength = _envelopeLength0 + _envelopeLength1 + _envelopeLength2;
      
      _envelopeOverLength0 = 1.0 / _envelopeLength0;
      _envelopeOverLength1 = 1.0 / _envelopeLength1;
      _envelopeOverLength2 = 1.0 / _envelopeLength2;
      
      if(!_noiseBuffer) {
        _noiseBuffer = new Array(32);
      }
      
      for(i = 0; i < 32; i++) {
        _noiseBuffer[i] = Math.random() * 2.0 - 1.0;
      }
      
      _repeatTime = 0;
      
      if (p.repeatSpeed == 0.0) {
        _repeatLimit = 0;
      } else {
        _repeatLimit = parseInt((1.0-p.repeatSpeed) * (1.0-p.repeatSpeed) * 20000) + 32;
      }
    }
  }
  
  /**
   * Writes the wave to the supplied buffer ByteArray
   * @param  buffer    A ByteArray to write the wave to
   * @param  waveData  If the wave should be written for the waveData
   * @return        If the wave is finished
   */
  this.synthWave = function synthWave(buffer, length)  {
    var _lpFilterOldPos, _periodTemp, _phaserInt, _pos, _repeatLimit, _repeatTime, _sample, _sampleCount, _superSample;
    for(var i = 0; i < length; i++) {
      // Repeats every _repeatLimit times, partially resetting the sound parameters
      if(_repeatLimit != 0) {
        if(++_repeatTime >= _repeatLimit) {
          _repeatTime = 0;
          this.reset(false);
        }
      }
      
      // If _changeLimit is reached, shifts the pitch
      if(_changeLimit != 0) {
        if(++_changeTime >= _changeLimit) {
          _changeLimit = 0;
          _period *= _changeAmount;
        }
      }
      
      // Acccelerate and apply slide
      _slide += _deltaSlide;
      _period *= _slide;
      
      // Checks for frequency getting too low, and stops the sound if a minFrequency was set
      if(_period > _maxPeriod) {
        _period = _maxPeriod;
        if(_minFreqency > 0.0) {
          return i;
        }
      }
      
      _periodTemp = _period;
      
      
      _periodTemp = parseInt(_periodTemp);
      if(_periodTemp < 8) {
        _periodTemp = 8;
      }
      
      // Sweeps the square duty
      if (_waveType == 0) {
        _squareDuty += _dutySweep;
        if(_squareDuty < 0.0) {
          _squareDuty = 0.0;
        } else if (_squareDuty > 0.5) {
          _squareDuty = 0.5;
        }
      }
      
      // Moves through the different stages of the volume envelope
      if(++_envelopeTime > _envelopeLength) {
        _envelopeTime = 0;
        
        switch(++_envelopeStage)  {
          case 1: 
            _envelopeLength = _envelopeLength1; 
            break;
          case 2:
             _envelopeLength = _envelopeLength2; 
             break;
        }
      }
      
      // Sets the volume based on the position in the envelope
      switch(_envelopeStage) {
        case 0: 
          _envelopeVolume = _envelopeTime * _envelopeOverLength0;
          break;
        case 1:
           _envelopeVolume = 1.0 + (1.0 - _envelopeTime * _envelopeOverLength1) * 2.0 * _sustainPunch; 
           break;
        case 2: 
           _envelopeVolume = 1.0 - _envelopeTime * _envelopeOverLength2;
           break;
        case 3: 
           _envelopeVolume = 0.0; return i;
           break;
      }
      
      
      // Moves the high-pass filter cutoff
      if(_filters && _hpFilterDeltaCutoff != 0.0) {
        _hpFilterCutoff *= _hpFilterDeltaCutoff;
        if(_hpFilterCutoff < 0.00001) {
          _hpFilterCutoff = 0.00001;
        } else if(_hpFilterCutoff > 0.1) {
          _hpFilterCutoff = 0.1;
        }
      }
      
      _superSample = 0.0;
      for(var j = 0; j < 8; j++) {
        // Cycles through the period
        _phase++;
        if(_phase >= _periodTemp) {
          _phase = _phase - _periodTemp;
          
          // Generates new random noise for this period
          if(_waveType == 3) { 
            for(var n = 0; n < 32; n++) {
              _noiseBuffer[n] = Math.random() * 2.0 - 1.0;
            }
          }
        }
        
        // Gets the sample from the oscillator
        switch(_waveType) {
          case 0: // Square wave
            _sample = ((_phase / _periodTemp) < _squareDuty) ? 0.5 : -0.5;
            break;
          case 3: // Noise
            _sample = _noiseBuffer[Math.abs(parseInt(_phase * 32 / parseInt(_periodTemp)))];
            break;
        }
        
        // Applies the low and high pass filters
        if (_filters) {
          _lpFilterOldPos = _lpFilterPos;
          _lpFilterCutoff *= _lpFilterDeltaCutoff;
          if(_lpFilterCutoff < 0.0) {
            _lpFilterCutoff = 0.0;
          } else if(_lpFilterCutoff > 0.1) {
            _lpFilterCutoff = 0.1;
          }

          if(_lpFilterOn) {
            _lpFilterDeltaPos += (_sample - _lpFilterPos) * _lpFilterCutoff;
            _lpFilterDeltaPos *= _lpFilterDamping;
          } else {
            _lpFilterPos = _sample;
            _lpFilterDeltaPos = 0.0;
          }
          
          _lpFilterPos += _lpFilterDeltaPos;
          
          _hpFilterPos += _lpFilterPos - _lpFilterOldPos;
          _hpFilterPos *= 1.0 - _hpFilterCutoff;
          _sample = _hpFilterPos;
        }
        
        _superSample += _sample;
      }
      
      // Averages out the super samples and applies volumes
      _superSample = _masterVolume * _envelopeVolume * _superSample * 0.125;
      
      // Clipping if too loud
      if(_superSample > 1.0) {
        _superSample = 1.0;
      } else if(_superSample < -1.0) {
        _superSample = -1.0;
      }
      
      // Writes mono wave data to the .wav format
      buffer[i] = parseInt(32000.0 * _superSample);
    }
    
    return length;
  }
}

SfxrSynth.prototype.getSfx = function(str) {
  // Initialize SfxrParams
  this._params.setSettingsString(str);

  // Synthesize Wave
  this.reset(true);
  this._envelopeFullLength = parseInt(this._envelopeFullLength);
  var samples = new Uint16Array(this._envelopeFullLength);
  var used = this.synthWave(samples, this._envelopeFullLength, false);
  return this.getWave(samples, used);
}

// Adapted from http://html5-demos.appspot.com/static/html5-whats-new/template/index.html#31
SfxrSynth.prototype.getWave = function(samples, length, channels) {
  var channels = channels || 1;
  // Initialize header
  var header = new Uint8Array([
    0x52,0x49,0x46,0x46, // 'RIFF'
    0, 0, 0, 0,          // put total size here
    0x57,0x41,0x56,0x45, // 'WAVE'
    0x66,0x6d,0x74,0x20, // 'fmt '
    16,0,0,0,            // size of the following
    1, 0,                // PCM format
    channels, 0,         // Mono: 1 channel or Stereo: 2 channels
    0x44,0xAC,0,0,       // 44,100 samples per second
    0,0,0,0,             // byte rate: two bytes per sample
    2*channels, 0,       // aligned on every two bytes
    16, 0,               // 16 bits per sample
    0x64,0x61,0x74,0x61, // 'data'
    0, 0, 0, 0           // put number of samples here
  ]);  // Note: we just want the ArrayBuffer.

  var soundLength = length * 2;
  var dv = new Uint32Array(header.buffer);
  dv[1] = 36 + soundLength;
  dv[7] = 44100 * channels * 2;
  dv[10] = soundLength;

  var blob = new Blob([header.buffer, samples.subarray(0, length-1).buffer], { 'type' : 'audio/wav' });
  
  var url = w.URL || w.webkitURL;
  return url.createObjectURL(blob);
}

//Exports for Closure
window['SfxrSynth'] = SfxrSynth; // <-- Constructor
SfxrSynth.prototype['getWave'] = SfxrSynth.prototype.getWave;
SfxrSynth.prototype['getSfx'] = SfxrSynth.prototype.getSfx;
