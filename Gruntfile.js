
module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        // compile scss
        sass: {
            dist: {
                options: {
                    style: 'compressed',
                    noCache: true
                },
                files: {
                    'wilbur/static/css/styles.css': 'wilbur/scss/styles.scss'
                }
            }
        },

        // autoprefix css
        autoprefixer: {
            dist: {
                files: {
                    'wilbur/static/css/styles.css': 'wilbur/static/css/styles.css'
                }
            }
        },

        // comb css
        csscomb: {
            options: {
                config: '.csscomb.json'
            },
            files: {
                'wilbur/static/css/styles.css': 'wilbur/static/css/styles.css'
            }
        },

        // compile coffee
        coffee : {
            compile: {
                expand: true,
                cwd: 'wilbur/coffee',
                src: ['*.coffee'],
                dest: 'wilbur/static/js/',
                ext: '.js'
            }
        },

        // watch for changes
        watch: {
            css: {
                files: ['wilbur/scss/**/*.scss'],
                tasks: ['sass', 'autoprefixer', 'csscomb'],
                options: {
                    interrupt: true,
                    spawn: false
                }
            },
            js: {
                files: ['wilbur/coffee/*.coffee'],
                tasks: ['coffee'],
                options: {
                    interrupt: true,
                    spawn: false
                }
            }
        }

    });

    // loads
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-autoprefixer');
    grunt.loadNpmTasks('grunt-csscomb');
    grunt.loadNpmTasks('grunt-contrib-coffee');
    grunt.loadNpmTasks('grunt-contrib-watch');

    // tasks
    grunt.registerTask('default', ['sass', 'autoprefixer', 'csscomb', 'coffee']);
};
