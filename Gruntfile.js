
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

        // compile coffee
        coffee : {
            compile: {
                files: {
                    'wilbur/static/js/coffeecounter.js': 'wilbur/coffee/coffeecounter.coffee',
                    'wilbur/static/js/confirm.js': 'wilbur/coffee/confirm.coffee',
                    'wilbur/static/js/filter.js': 'wilbur/coffee/filter.coffee',
                    'wilbur/static/js/minical.js': 'wilbur/coffee/minical.coffee',
                    'wilbur/static/js/niceselect.js': 'wilbur/coffee/niceselect.coffee',
                    'wilbur/static/js/niceselectdate.js': 'wilbur/coffee/niceselectdate.coffee',
                    'wilbur/static/js/validator.js': 'wilbur/coffee/validator.coffee'
                }
            }
        },

        // watch for changes
        watch: {
            css: {
                files: ['wilbur/scss/**/*.scss'],
                tasks: ['sass', 'autoprefixer'],
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
    grunt.loadNpmTasks('grunt-contrib-coffee');
    grunt.loadNpmTasks('grunt-contrib-watch');

    // tasks
    grunt.registerTask('default', ['sass', 'autoprefixer', 'coffee']);
};
