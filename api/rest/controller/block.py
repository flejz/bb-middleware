from flask import jsonify, request

def init(app, block_handler):

    @app.route("/chain", methods=["GET", "POST"])
    def chain():
        if request.method == "GET":
            chain = block_handler.get_chain()
            blocks = list(map(block_handler.get_block, chain))
            return jsonify(blocks)
        elif request.method == "POST":
            return block_handler.add_block(request.json)

        return None

    @app.route("/block/<block_hash>")
    def get_block(block_hash):
        return block_handler.get_block(block_hash)
