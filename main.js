class BootScene extends Phaser.Scene {
    constructor() {
        super('BootScene');
    }
    preload() {
        // Load ship parts
        const loadRange = (prefix, count) => {
            for (let i = 1; i <= count; i++) {
                this.load.image(`${prefix}${i}`, `sprites/${prefix}${i}.png`);
            }
        };
        loadRange('engine', 10);
        loadRange('cabin', 21);
        loadRange('storagetop', 9);
        loadRange('storagebottom', 10);
        loadRange('gun', 10);
        loadRange('logo', 14);
        loadRange('pipes', 10);
        loadRange('wires', 7);
        loadRange('flame', 4);
        loadRange('flamebig', 4);
        loadRange('exp', 6);
        this.load.image('base1', 'sprites/base1.png');
        this.load.image('hud', 'sprites/hud.png');
        this.load.image('buildingship', 'sprites/buildingship.png');
        this.load.image('gameover', 'sprites/gameover.png');
    }
    create() {
        this.scene.start('BuildScene');
    }
}

class BuildScene extends Phaser.Scene {
    constructor() { super('BuildScene'); }
    create() {
        this.add.image(160, 120, 'buildingship');
        this.buildText = this.add.text(160, 210, '', { font: '16px monospace', fill: '#fff' }).setOrigin(0.5);
        this.ship = this.add.container((320-99)/2, (240-60)/2);
        this.parts = {
            base: this.add.image(0,0,'base1').setOrigin(0,0),
            engine_top: this.add.image(0,0,null).setOrigin(0,0),
            storage_top: this.add.image(33,0,null).setOrigin(0,0),
            cabin: this.add.image(66,0,null).setOrigin(0,0),
            engine_bottom: this.add.image(0,30,null).setOrigin(0,0),
            storage_bottom: this.add.image(33,30,null).setOrigin(0,0),
            gun: this.add.image(66,30,null).setOrigin(0,0),
            logo: this.add.image(0,0,null).setOrigin(0,0),
            pipes: this.add.image(0,0,null).setOrigin(0,0),
            wires: this.add.image(0,0,null).setOrigin(0,0)
        };
        Object.values(this.parts).forEach(p => this.ship.add(p));
        this.buildSteps = [
            ['engine_top', 'engine', 9, 'TUNING TOP ENGINE'],
            ['engine_bottom', 'engine', 10, 'SPOOLING BOTTOM ENGINE'],
            ['storage_top', 'storagetop', 9, 'BOLTING ON TOP STORAGE'],
            ['storage_bottom', 'storagebottom', 10, 'GLUEING ON BOTTOM STORAGE'],
            ['cabin', 'cabin', 21, 'PUTTING SEATS IN'],
            ['gun', 'gun', 10, 'LOADING GUNS'],
            ['logo', 'logo', 14, 'CUSTOMISATION'],
            ['wires', 'wires', 7, 'WIRING ENGINE'],
            ['pipes', 'pipes', 10, 'FINAL COOLING SYSTEMS']
        ];
        this.stepIndex = 0;
        this.time.delayedCall(500, () => this.runStep());
    }
    runStep() {
        if (this.stepIndex >= this.buildSteps.length) {
            this.buildText.setText('LAUNCHING');
            this.time.delayedCall(1000, () => this.scene.start('GameScene', {textures: this.parts}));
            return;
        }
        const [key, prefix, max, msg] = this.buildSteps[this.stepIndex];
        this.buildText.setText(msg);
        const part = this.parts[key];
        const timer = this.time.addEvent({
            delay: 50,
            callback: () => {
                const idx = Phaser.Math.Between(1, max);
                part.setTexture(`${prefix}${idx}`);
            },
            repeat: 19
        });
        this.time.delayedCall(1000, () => {
            timer.remove(false);
            const idx = Phaser.Math.Between(1, max);
            part.setTexture(`${prefix}${idx}`);
            this.stepIndex++;
            this.time.delayedCall(100, () => this.runStep());
        });
    }
}

class GameScene extends Phaser.Scene {
    constructor(){ super('GameScene'); }
    init(data){ this.startParts = data.textures; }
    create(){
        // starfield
        this.star1 = this.add.tileSprite(160,120,320,240, this.createStarTexture(50));
        this.star2 = this.add.tileSprite(160,120,320,240, this.createStarTexture(100));

        // ship
        this.ship = this.add.container((320-99)/2, (240-60)/2);
        this.parts = {};
        for (const [k,img] of Object.entries(this.startParts)){
            this.parts[k] = this.add.image(img.x, img.y, img.texture.key).setOrigin(0,0);
            this.ship.add(this.parts[k]);
        }
        // flames
        this.anims.create({ key:'flame', frames:[{key:'flame1'},{key:'flame2'},{key:'flame3'},{key:'flame4'}], frameRate:8, repeat:-1});
        this.anims.create({ key:'flamebig', frames:[{key:'flamebig1'},{key:'flamebig2'},{key:'flamebig3'},{key:'flamebig4'}], frameRate:8, repeat:-1});
        this.flameTop = this.add.sprite(-10,15,'flame1').setOrigin(0,0);
        this.flameBottom = this.add.sprite(-10,45,'flame1').setOrigin(0,0);
        this.ship.addAt(this.flameTop,0);
        this.ship.addAt(this.flameBottom,0);
        this.flameTop.play('flame');
        this.flameBottom.play('flame');
        this.speed = 1;
        this.boost = 100;
        this.damage = 0;
        this.distance = 0;
        this.statusMessages = ['All systems nominal','Scanning sector','Solar panels charged','Awaiting commands'];
        this.statusIndex = 0;
        this.statusText = this.add.text(160,5,'',{font:'14px monospace',fill:'#0f0'}).setOrigin(0.5,0);
        this.hudText = this.add.text(5,220,'', {font:'14px monospace',fill:'#fff'});
        this.updateHUD();
        this.time.addEvent({delay:5000, callback:()=>{ this.statusIndex=(this.statusIndex+1)%this.statusMessages.length; this.updateHUD();}, loop:true});
        this.time.addEvent({delay:15000, callback:()=>this.triggerEvent(), loop:true});
        this.input.keyboard.on('keydown-SPACE', () => this.toggleBoost());
    }
    createStarTexture(count){
        const rt = this.add.renderTexture(0,0,320,240);
        const g = this.make.graphics({x:0,y:0,add:false});
        g.fillStyle(0xffffff);
        for(let i=0;i<count;i++){ g.fillRect(Phaser.Math.Between(0,319), Phaser.Math.Between(0,239),2,2); }
        rt.draw(g);
        const key = 'stars'+count+Phaser.Math.RND.uuid();
        rt.saveTexture(key);
        rt.destroy();
        return key;
    }
    update(){
        const move = this.speed * (this.boostActive?2:1);
        this.star1.tilePositionX += move*0.5;
        this.star2.tilePositionX += move;
        if(this.boostActive){
            this.boost -= 0.1;
            if(this.boost <= 0){ this.boost = 0; this.toggleBoost(false); }
        }
        this.distance += move*0.1;
        this.updateHUD();
    }
    updateHUD(){
        this.statusText.setText(this.statusMessages[this.statusIndex]);
        this.hudText.setText(`Boost:${this.boost.toFixed(0)}  Damage:${this.damage}  Speed:${this.speed*(this.boostActive?2:1)}  Distance:${this.distance.toFixed(0)}`);
    }
    toggleBoost(forceOff){
        if(forceOff){ this.boostActive=false; this.flameTop.play('flame'); this.flameBottom.play('flame'); return; }
        if(this.boost>0){
            this.boostActive=!this.boostActive;
            if(this.boostActive){ this.flameTop.play('flamebig'); this.flameBottom.play('flamebig'); } else { this.flameTop.play('flame'); this.flameBottom.play('flame'); }
        }
    }
    triggerEvent(){
        this.scene.pause();
        const event = {title:'Random Event', desc:'Something happens in space.', successRate:0.5};
        const panel = this.add.rectangle(160,120,300,140,0x000000,0.8);
        const title = this.add.text(160,80,event.title,{font:'16px monospace',fill:'#fff'}).setOrigin(0.5);
        const desc = this.add.text(160,110,event.desc,{font:'14px monospace',fill:'#fff',align:'center',wordWrap:{width:280}}).setOrigin(0.5,0);
        const btnSuccess = this.add.text(100,170,'OK',{font:'16px monospace',fill:'#0f0'}).setInteractive();
        const btnFail = this.add.text(220,170,'Ignore',{font:'16px monospace',fill:'#f00'}).setInteractive();
        btnSuccess.on('pointerdown',()=>finish(true));
        btnFail.on('pointerdown',()=>finish(Math.random()<event.successRate));
        const finish = (success)=>{
            panel.destroy(); title.destroy(); desc.destroy(); btnSuccess.destroy(); btnFail.destroy();
            if(success){ this.boost=Math.min(100,this.boost+10); }
            else { this.damage+=10; if(this.damage>=100){ this.flashAndExplode(); return; } }
            this.scene.resume();
        };
    }
    flashAndExplode(){
        this.cameras.main.flash(500,255,255,255);
        this.anims.create({ key:'explode', frames:[{key:'exp1'},{key:'exp2'},{key:'exp3'},{key:'exp4'},{key:'exp5'},{key:'exp6'}], frameRate:10 });
        const boom = this.add.sprite(160,120,'exp1');
        boom.play('explode');
        boom.on('animationcomplete', () => {
            boom.destroy();
            this.add.image(160,120,'gameover');
            this.input.keyboard.once('keydown-SPACE', () => location.reload());
        });
    }
}

const config = {
    type: Phaser.AUTO,
    width: 320,
    height: 240,
    backgroundColor: '#000',
    pixelArt: true,
    scene: [BootScene, BuildScene, GameScene]
};

new Phaser.Game(config);